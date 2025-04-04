import os
import json
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import erniebot

# 加载环境变量
load_dotenv()

# 设置文心一言API配置
erniebot.api_type = "aistudio"
erniebot.access_token = os.getenv("ERNIE_ACCESS_TOKEN")

# 城市名称映射
CITY_MAP = {
    "上海": "Shanghai",
    "北京": "Beijing",
    "广州": "Guangzhou",
    "深圳": "Shenzhen",
    "杭州": "Hangzhou",
    "南京": "Nanjing",
    "成都": "Chengdu",
    "武汉": "Wuhan",
    "西安": "Xian",
    "重庆": "Chongqing",
    "天津": "Tianjin",
    "苏州": "Suzhou",
    "厦门": "Xiamen",
    "青岛": "Qingdao",
    "大连": "Dalian"
}

class WeatherAgent:
    def __init__(self):
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.weather_api_url = "http://api.weatherapi.com/v1/forecast.json"
        
    def parse_user_intent(self, user_query):
        """使用文心一言API解析用户意图"""
        prompt = f"""
        分析以下用户查询，提取关键信息：
        查询：{user_query}
        
        请以JSON格式返回以下信息：
        - location: 地点
        - time: 时间（今天/明天/后天）
        - concerns: 用户关心的天气要素（如：温度、降水、风力等）
        """
        
        try:
            response = erniebot.ChatCompletion.create(
                model="ernie-lite",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # 尝试从响应中提取JSON
            result = response.get_result()
            try:
                # 如果结果已经是JSON字符串，直接解析
                return json.loads(result)
            except json.JSONDecodeError:
                # 如果结果不是JSON字符串，尝试从文本中提取JSON部分
                import re
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    # 如果无法提取JSON，返回一个基本的结构
                    return {
                        "location": "上海",  # 默认值
                        "time": "今天",      # 默认值
                        "concerns": ["天气"]  # 默认值
                    }
        except Exception as e:
            print(f"解析用户意图时出错：{str(e)}")
            # 返回默认值
            return {
                "location": "上海",
                "time": "今天",
                "concerns": ["天气"]
            }
    
    def get_weather_data(self, location, date):
        """获取天气数据"""
        # 转换中文城市名为英文
        location_en = CITY_MAP.get(location, location)
        
        params = {
            "key": self.weather_api_key,
            "q": location_en,
            "days": 3,
            "aqi": "no"
        }
        
        try:
            response = requests.get(self.weather_api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # 根据日期选择对应的天气数据
            if date == "今天":
                return data["forecast"]["forecastday"][0]
            elif date == "明天":
                return data["forecast"]["forecastday"][1]
            elif date == "后天":
                return data["forecast"]["forecastday"][2]
            else:
                return data["forecast"]["forecastday"][0]
                
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def generate_response(self, weather_data, user_intent):
        """生成自然语言回复"""
        if "error" in weather_data:
            return f"抱歉，获取天气数据时出现错误：{weather_data['error']}"
            
        # 提取关键天气信息
        day = weather_data.get("day", {})
        temp_c = day.get("avgtemp_c", "未知")
        condition = day.get("condition", {}).get("text", "未知")
        rain_chance = day.get("daily_chance_of_rain", "未知")
        max_wind_kph = day.get("maxwind_kph", "未知")
        
        weather_summary = {
            "温度": f"{temp_c}°C",
            "天气": condition,
            "降雨概率": f"{rain_chance}%",
            "最大风速": f"{max_wind_kph}km/h"
        }
            
        prompt = f"""
        地点：{user_intent['location']}
        时间：{user_intent['time']}
        天气：{json.dumps(weather_summary, ensure_ascii=False)}
        
        请根据以上天气信息，生成一个简短的建议。
        """
        
        try:
            response = erniebot.ChatCompletion.create(
                model="ernie-lite",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.get_result()
        except Exception as e:
            print(f"生成回复时出错：{str(e)}")
            return "抱歉，我暂时无法生成回复。请稍后再试。"
    
    def process_query(self, user_query):
        """处理用户查询的主函数"""
        try:
            # 解析用户意图
            user_intent = self.parse_user_intent(user_query)
            
            # 获取天气数据
            weather_data = self.get_weather_data(
                user_intent["location"],
                user_intent["time"]
            )
            
            # 生成回复
            response = self.generate_response(weather_data, user_intent)
            
            return response
        except Exception as e:
            print(f"处理查询时出错：{str(e)}")
            return "抱歉，处理您的查询时出现错误。请稍后再试。"

def main():
    # 创建WeatherAgent实例
    agent = WeatherAgent()
    
    print("欢迎使用智能天气助手！输入'退出'结束对话。")
    
    while True:
        user_query = input("\n请输入您的天气查询：")
        if user_query.lower() in ['退出', 'quit', 'exit']:
            break
            
        response = agent.process_query(user_query)
        print("\n助手回复：", response)

if __name__ == "__main__":
    main() 