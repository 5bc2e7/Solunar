# main.py (V4.2 - 修正版)

from fastapi import FastAPI, Query
from skyfield.api import load, Topos
from skyfield import almanac
from datetime import date, datetime, timedelta
import pytz # 用于时区处理

# --- 全局资源加载 ---
print("Loading astronomical data...")
ts = load.timescale()
# 使用更新、更小、精度相同的DE440s星历表
eph = load('de440s.bsp')
print("Astronomical data loaded successfully.")

# --- FastAPI 应用实例 ---
app = FastAPI(
    title="轻量天文API",
    description="一个轻量、快速的API，提供日出日落、月相信息，并支持时区转换。",
    version="4.2.0", # 版本号更新
)

# --- 辅助函数 ---

def get_moon_phase_name(illumination_percent: float, moon_phase_orbital_degrees: float) -> str:
    """
    根据月球的照亮百分比和月龄轨道角度（0-360度）判断月相名称。
    moon_phase_orbital_degrees: 0=新月, 90=上弦月, 180=满月, 270=下弦月
    """
    
    # 极小或极大的百分比，直接判断新月和满月
    if illumination_percent < 0.5: # 接近0%
        return "新月 (New Moon)"
    if illumination_percent > 99.5: # 接近100%
        return "满月 (Full Moon)"

    # 判断盈亏 (Waxing/Waning)
    # 月龄角度 0-180度为盈 (Waxing)，180-360度为亏 (Waning)
    is_waxing = moon_phase_orbital_degrees <= 180

    # 判断弦月 (First/Last Quarter) - 50% 照亮
    # 给出1%的容错范围，以处理浮点数精度和常见的定义
    if 49 <= illumination_percent <= 51: 
        if is_waxing:
            return "上弦月 (First Quarter)" # 50% 照亮且在变亮
        else:
            return "下弦月 (Last Quarter)" # 50% 照亮且在变暗
    
    # 判断蛾眉月 (Crescent) 或 凸月 (Gibbous)
    elif illumination_percent < 50: # 少于50%照亮
        if is_waxing:
            return "蛾眉月 (Waxing Crescent)" # 正在变亮的新月和上弦月之间
        else:
            return "残月 (Waning Crescent)" # 正在变暗的下弦月和新月之间 (也叫亏眉月)
    else: # 大于50%照亮
        if is_waxing:
            return "盈凸月 (Waxing Gibbous)" # 正在变亮的上弦月和满月之间
        else:
            return "亏凸月 (Waning Gibbous)" # 正在变暗的满月和下弦月之间

def convert_to_timezone(time_str: str, tz_name: str):
    """将UTC时间字符串转换为指定时区的时间字符串"""
    if not time_str or not tz_name:
        return time_str
    try:
        target_tz = pytz.timezone(tz_name)
        # 兼容'Z'后缀的ISO格式
        utc_dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        local_dt = utc_dt.astimezone(target_tz)
        return local_dt.isoformat()
    except pytz.UnknownTimeZoneError:
        # 如果时区名称无效，返回原始UTC时间字符串
        print(f"Warning: Unknown timezone '{tz_name}'. Returning UTC time.")
        return time_str
    except Exception as e:
        print(f"Error converting time '{time_str}' to timezone '{tz_name}': {e}")
        return time_str

# --- API 端点 ---

@app.get("/")
def read_root():
    return {"message": "欢迎使用轻量天文API！请访问 /docs 查看详情。"}

@app.get("/api/sun")
def get_sun_times(
    lat: float = Query(..., description="纬度，例如：21.5 (北部湾)", ge=-90, le=90),
    lon: float = Query(..., description="经度，例如：108.5 (北部湾)", ge=-180, le=180),
    target_date: date = Query(None, description="目标日期 (YYYY-MM-DD)，默认为今天"),
    tz: str = Query("UTC", description="输出时区，例如 Asia/Shanghai 或 UTC")
):
    """计算指定地点的日出、日落和正午时间。"""
    if target_date is None:
        target_date = date.today()

    observer_topos = Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    # 获取目标时区对象
    tz_obj = pytz.timezone(tz)
    
    # 构建目标日期在目标时区下的午夜时间 (00:00:00)
    local_midnight_start = tz_obj.localize(datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0))
    
    # 将本地午夜时间转换为 Skyfield 的 UTC 时间对象作为搜索起始点
    utc_start_dt = local_midnight_start.astimezone(pytz.utc)
    t0 = ts.utc(utc_start_dt.year, utc_start_dt.month, utc_start_dt.day,
                utc_start_dt.hour, utc_start_dt.minute, utc_start_dt.second)
    
    # 搜索窗口为从 t0 开始的 24 小时 (即 t0 + 1 天)
    t1 = t0 + 1 

    # 获取太阳对象
    sun = eph['sun']

    # 查找日出和日落
    times, events = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, observer_topos))
    
    results_utc = {"sunrise": None, "noon": None, "sunset": None}
    
    for t, event in zip(times, events):
        event_date_in_tz = tz_obj.normalize(t.astimezone(tz_obj)).date()
        if event_date_in_tz == target_date:
            if event == 1 and results_utc["sunrise"] is None: # 0->1 是日出
                results_utc["sunrise"] = t.utc_iso()
            elif event == 0 and results_utc["sunset"] is None: # 1->0 是日落
                results_utc["sunset"] = t.utc_iso()

    # 查找正午（太阳过中天）
    # almanac.meridian_transits 返回一个函数，该函数在目标过中天时返回1（上中天）或-1（下中天）
    noon_function = almanac.meridian_transits(eph, sun, observer_topos)
    noon_times, noon_events = almanac.find_discrete(t0, t1, noon_function)

    if noon_times:
        for i, noon_t in enumerate(noon_times):
            # 确保是上中天（事件值为1）并且是目标日期内的事件
            if noon_events[i] == 1: # 1表示上中天（即正午）
                noon_date_in_tz = tz_obj.normalize(noon_t.astimezone(tz_obj)).date()
                if noon_date_in_tz == target_date:
                    results_utc["noon"] = noon_t.utc_iso()
                    break # 找到正确的正午，退出循环
    
    # 将所有UTC时间转换为指定时区
    results_local = {key: convert_to_timezone(value, tz) for key, value in results_utc.items()}
    
    return {
        "location": {"latitude": lat, "longitude": lon},
        "date": target_date.isoformat(),
        "timezone": tz,
        "times": results_local
    }

@app.get("/api/moon")
def get_moon_info(
    lat: float = Query(..., description="纬度，例如：39.9 (北京)", ge=-90, le=90),
    lon: float = Query(..., description="经度，例如：116.4 (北京)", ge=-180, le=180),
    target_date: date = Query(None, description="目标日期 (YYYY-MM-DD)，默认为今天"),
    tz: str = Query("UTC", description="输出时区，例如 Asia/Shanghai 或 UTC")
):
    """计算指定地点的月出、月落、中天时间，并提供当日的月相信息。"""
    if target_date is None:
        target_date = date.today()

    observer_topos = Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    try:
        tz_obj = pytz.timezone(tz)
    except pytz.UnknownTimeZoneError:
        tz_obj = pytz.utc
        tz = "UTC"

    local_midnight_start = tz_obj.localize(datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0))
    utc_start_dt = local_midnight_start.astimezone(pytz.utc)
    t0 = ts.utc(utc_start_dt.year, utc_start_dt.month, utc_start_dt.day,
                utc_start_dt.hour, utc_start_dt.minute, utc_start_dt.second)
    t1 = t0 + 1

    moon = eph['moon']

    # 查找月出和月落
    f = almanac.risings_and_settings(eph, moon, observer_topos)
    times, events = almanac.find_discrete(t0, t1, f)

    results_utc = {"moonrise": None, "moontransit": None, "moonset": None}

    for t, event in zip(times, events):
        event_date_in_tz = tz_obj.normalize(t.astimezone(tz_obj)).date()
        if event_date_in_tz == target_date:
            if event == 1 and results_utc["moonrise"] is None: # 1 是升起
                results_utc["moonrise"] = t.utc_iso()
            elif event == 0 and results_utc["moonset"] is None: # 0 是降落
                results_utc["moonset"] = t.utc_iso()

    # 查找中天
    transit_function = almanac.meridian_transits(eph, moon, observer_topos)
    transit_times, transit_events = almanac.find_discrete(t0, t1, transit_function)

    noon_t_for_phase = None
    if transit_times:
        for i, transit_t in enumerate(transit_times):
            if transit_events[i] == 1: # 1表示上中天
                transit_date_in_tz = tz_obj.normalize(transit_t.astimezone(tz_obj)).date()
                if transit_date_in_tz == target_date:
                    results_utc["moontransit"] = transit_t.utc_iso()
                    noon_t_for_phase = transit_t # 使用中天时间计算月相
                    break
    
    if noon_t_for_phase is None:
        noon_t_for_phase = ts.utc(target_date.year, target_date.month, target_date.day, 12)

    # --- 月相计算 ---
    sun_moon_earth_angle = almanac.phase_angle(eph, 'moon', noon_t_for_phase)
    illumination_fraction = almanac.fraction_illuminated(eph, 'moon', noon_t_for_phase)
    moon_phase_orbital_angle = almanac.moon_phase(eph, noon_t_for_phase)
    
    sun_moon_earth_angle_degrees = round(sun_moon_earth_angle.degrees, 2)
    illumination_percent = round(illumination_fraction * 100, 2)
    moon_phase_orbital_degrees = round(moon_phase_orbital_angle.degrees, 2)
    phase_name = get_moon_phase_name(illumination_percent, moon_phase_orbital_degrees)

    # 转换时区
    results_local = {key: convert_to_timezone(value, tz) for key, value in results_utc.items()}

    return {
        "location": {"latitude": lat, "longitude": lon},
        "date": target_date.isoformat(),
        "timezone": tz,
        "times": results_local,
        "phase_info_at_transit": {
            "timestamp_for_phase_calc": convert_to_timezone(noon_t_for_phase.utc_iso(), tz),
            "sun_moon_earth_angle_degrees": sun_moon_earth_angle_degrees,
            "moon_phase_orbital_degrees": moon_phase_orbital_degrees,
            "illumination_percent": illumination_percent,
            "phase_name": phase_name
        }
    }

