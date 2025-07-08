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
def get_moon_phase(
    tz: str = Query("UTC", description="输出时区，例如 Asia/Shanghai 或 UTC")
):
    """获取当前的月相信息。"""
    t = ts.now() # 获取当前时间

    # 太阳-月球-地球夹角 (0-180度)，直接影响照亮百分比
    # 0度=新月，180度=满月
    sun_moon_earth_angle = almanac.phase_angle(eph, 'moon', t) 
    
    # 月球被照亮的百分比 (0.0到1.0之间的分数)
    illumination_fraction = almanac.fraction_illuminated(eph, 'moon', t) # 返回的是浮点数
    
    # 月龄轨道角度 (0-360度)，这是月球在其轨道上相对于太阳的黄经差
    # 0度=新月，90度=上弦月，180度=满月，270度=下弦月
    moon_phase_orbital_angle = almanac.moon_phase(eph, t) 
    
    # 提取并四舍五入值
    sun_moon_earth_angle_degrees = round(sun_moon_earth_angle.degrees, 2)
    illumination_percent = round(illumination_fraction * 100, 2) # 修正: 直接乘以100
    moon_phase_orbital_degrees = round(moon_phase_orbital_angle.degrees, 2)

    # 根据照亮百分比和月龄角度获取月相名称
    phase_name = get_moon_phase_name(illumination_percent, moon_phase_orbital_degrees)
    
    return {
        "timestamp": convert_to_timezone(t.utc_iso(), tz),
        "timezone": tz,
        "sun_moon_earth_angle_degrees": sun_moon_earth_angle_degrees, # 太阳-月球-地球夹角，影响亮度
        "moon_phase_orbital_degrees": moon_phase_orbital_degrees, # 月球在轨道上的角度，用于判断盈亏
        "illumination_percent": illumination_percent,
        "phase_name": phase_name
    }

