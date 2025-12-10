import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import base64
import os

# --- 1. 工具函数：处理本地图片给地图弹窗使用 ---
def get_img_as_base64(file_path):
    """
    将本地图片转换为Base64字符串，以便在Folium的HTML弹窗中显示。
    如果找不到文件，返回一个占位符或空。
    """
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- 2. 页面基础设置 ---
st.set_page_config(layout="wide", page_title="中国濒危动物 StoryMap")

st.markdown("""
<style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    h1 {margin-top: 0;}
    /* 故事卡样式 */
    .story-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-family: sans-serif;
    }
    .stat-box {
        background-color: #e8f4f8;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-size: 0.9em;
    }
    .danger-box {
        background-color: #fbeaea;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-size: 0.9em;
        color: #842029;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 准备数据 (10个动物) ---
# 注意：location 坐标是根据栖息地描述估算的中心点
story_points = [
    {
        "title": "Giant Panda (大熊猫)",
        "subtitle": "Ailuropoda melanoleuca",
        "image_file": "panda.jpg",
        "location": [30.8, 103.0], # 四川/陕西交界
        "zoom": 7,
        "icon": "paw",
        "color": "black",
        "bio": "体重200-300磅的中型熊类，拥有独特的黑白花纹。虽然消化系统是食肉动物，但99%的食物是竹子，每天需进食26-84磅。它们有类似拇指的腕骨用于抓握竹子。",
        "habitat": "四川、陕西、甘肃的山区森林 (海拔1200-3400米)。",
        "population": "2005: 1,596 → 2023: 1,900 (+19%) | 趋势：增长中 (INCREASING) ✓",
        "danger": "基础设施导致的栖息地破碎化，对竹子的极度依赖，低繁殖率，以及气候变化威胁竹林生长。"
    },
    {
        "title": "Yangtze Finless Porpoise (江豚)",
        "subtitle": "Neophocaena asiaeorientalis",
        "image_file": "jiangtun.jpg",
        "location": [29.5, 116.0], # 长江中下游/鄱阳湖区域
        "zoom": 7,
        "icon": "tint", # 水滴或水相关
        "color": "blue",
        "bio": "世界上唯一的淡水鼠海豚，没有背鳍，头部圆润，看起来像在微笑。智商极高且群居，每15-20秒浮出水面呼吸。",
        "habitat": "长江中下游干流及鄱阳湖、洞庭湖。",
        "population": "2006: 1,800 → 2022: 1,249 (-31%) | 趋势：严重衰退后正在恢复 (RECOVERING) ↗",
        "danger": "渔网误捕，船只撞击，水利工程影响，水污染，以及过度捕捞导致的食物短缺。"
    },
    {
        "title": "South China Tiger (华南虎)",
        "subtitle": "Panthera tigris amoyensis",
        "image_file": "dongbeihu.jpg", # 使用提供的老虎图片
        "location": [27.0, 116.0], # 历史分布区：福建/江西山区
        "zoom": 6,
        "icon": "ban", #以此表示野外灭绝
        "color": "orange",
        "bio": "最濒危的老虎亚种。曾经是控制猎物数量的顶级掠食者，现在野外已无确其踪迹，仅剩圈养个体。",
        "habitat": "历史上分布于湖南、广东、福建、江西的山地森林。现无野外种群。",
        "population": "野外数量: 0 | 趋势：野外功能性灭绝 (FUNCTIONALLY EXTINCT) ×",
        "danger": "历史上的过度捕杀，栖息地大规模丧失(90%+)，猎物枯竭，以及近亲繁殖导致的基因瓶颈。"
    },
    {
        "title": "Golden Snub-nosed Monkey (川金丝猴)",
        "subtitle": "Rhinopithecus roxellana",
        "image_file": "jinsihou.jpg",
        "location": [33.5, 108.0], # 秦岭区域
        "zoom": 7,
        "icon": "tree",
        "color": "gold",
        "bio": "因朝天鼻和金色毛发得名，能忍受-10°C的低温。它们是群居动物，有时会形成数百只的大群。",
        "habitat": "四川、陕西、甘肃、湖北的高山森林 (海拔1500-3400米)。",
        "population": "2005: 15,000 → 2023: 23,000 (+53%) | 趋势：增长中 (INCREASING) ↗",
        "danger": "道路和水坝导致的栖息地破碎化，非法伐木，气候变化导致栖息地向高处迁移。"
    },
    {
        "title": "Crested Ibis (朱鹮)",
        "subtitle": "Nipponia nippon",
        "image_file": "zhuxuan.jpg",
        "location": [33.3, 107.5], # 陕西洋县
        "zoom": 8,
        "icon": "feather",
        "color": "red",
        "bio": "拥有红色的面部皮肤和优雅的冠羽。繁殖期会分泌灰色粉末将羽毛染灰。曾被认为已灭绝，1981年仅发现7只。",
        "habitat": "陕西、河南、浙江的稻田、湿地和森林混合区。",
        "population": "1981: 7 → 2023: 5,000 (+71,329%) | 趋势：奇迹般恢复 (DRAMATIC RECOVERY) ↑↑",
        "danger": "极度严重的基因瓶颈，对农药非常敏感，对特定栖息地组合（高树+湿地）的依赖。"
    },
    {
        "title": "Snow Leopard (雪豹)",
        "subtitle": "Panthera uncia",
        "image_file": "xuebao.jpg",
        "location": [34.5, 98.0], # 三江源/青海区域
        "zoom": 6,
        "icon": "snowflake",
        "color": "lightgray",
        "bio": "高海拔的幽灵，拥有厚实的毛皮和极长的尾巴（用于平衡和保暖）。巨大的脚掌像雪鞋一样。",
        "habitat": "西藏、青海、新疆的高山裸岩地带 (海拔3000-5500米)。",
        "population": "2005: 2,000 → 2023: 2,400 (+20%) | 趋势：稳中有升 (STABLE) →↗",
        "danger": "人兽冲突（报复性猎杀），非法盗猎，过度放牧导致的栖息地退化及气候变化。"
    },
    {
        "title": "Chinese Alligator (扬子鳄)",
        "subtitle": "Alligator sinensis",
        "image_file": "yangzie.jpg", # 对应提供的 alligater 图片
        "location": [30.9, 118.0], # 安徽宣城附近
        "zoom": 8,
        "icon": "eye",
        "color": "green",
        "bio": "世界上体型最小的鳄鱼之一，性情相对温顺。冬季（11月-3月）会在洞穴中冬眠。",
        "habitat": "安徽、浙江的长江下游缓流淡水区（池塘、稻田）。",
        "population": "野外: 200只 (圈养约1万只) | 趋势：缓慢增长 (SLOWLY INCREASING) ↗",
        "danger": "95%以上的栖息地因农业开发丧失，水污染，以及冬眠洞穴被破坏。"
    },
    {
        "title": "Asian Elephant (亚洲象)",
        "subtitle": "Elephas maximus",
        "image_file": "yazhouxiang.jpg",
        "location": [22.0, 100.8], # 云南西双版纳
        "zoom": 8,
        "icon": "star",
        "color": "darkgreen",
        "bio": "中国最大的陆生哺乳动物。高度群居，由雌性首领带领。它们是生态系统的工程师。",
        "habitat": "云南南部（西双版纳、普洱）的热带/亚热带雨林。",
        "population": "2005: 250 → 2023: 300 (+20%) | 趋势：增长后趋稳 (STABLE) ↗→",
        "danger": "极其有限的栖息地（<3000平方公里），剧烈的人象冲突（吃庄稼），以及基因交流受阻。"
    },
    {
        "title": "Tibetan Antelope (藏羚羊)",
        "subtitle": "Pantholops hodgsonii",
        "image_file": "zanglingyang.jpg",
        "location": [35.0, 89.0], # 可可西里
        "zoom": 6,
        "icon": "road", # 代表迁徙
        "color": "beige",
        "bio": "青藏高原的标志性物种，雄性有长角。以每年长距离迁徙产仔而闻名，奔跑速度可达80km/h。",
        "habitat": "青海、西藏、新疆的高寒草原 (海拔3700-5500米)，如可可西里。",
        "population": "2005: 7.5万 → 2023: 20万 (+167%) | 趋势：显著恢复 (DRAMATIC RECOVERY) ↑↑",
        "danger": "历史上因“沙图什”披肩导致的疯狂盗猎，现在面临铁路阻断迁徙路线及气候变化的威胁。"
    },
    {
        "title": "Hainan Gibbon (海南长臂猿)",
        "subtitle": "Nomascus hainanus",
        "image_file": "changbiyuan.jpg",
        "location": [19.1, 109.1], # 海南霸王岭
        "zoom": 9,
        "icon": "music", # 善于鸣叫
        "color": "black",
        "bio": "世界上最稀有的灵长类动物。完全树栖，通过独特的歌声来沟通领地。实行一夫一妻制。",
        "habitat": "仅存于海南岛霸王岭国家级自然保护区的热带雨林。",
        "population": "1950s: 2,000 → 2005: 13 → 2023: 37 | 趋势：极度濒危但缓慢恢复 (SLOWLY RECOVERING) ↗",
        "danger": "毁灭性的栖息地丧失（99%雨林被毁），种群极小导致抗灾难能力差，基因多样性匮乏。"
    }
]

# --- 4. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.step = 0

def next_step():
    if st.session_state.step < len(story_points) - 1:
        st.session_state.step += 1

def prev_step():
    if st.session_state.step > 0:
        st.session_state.step -= 1

# 获取当前选中的数据
current_data = story_points[st.session_state.step]

# --- 5. 页面布局 ---
st.title("🇨🇳 中国濒危动物 StoryMap")
col1, col2 = st.columns([2, 1.2], gap="medium")

with col1:
    # --- 左侧：地图 ---
    tile_url = "https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}@2x.png?api_key=6e0e8bbd-0a37-467c-b601-d28e409c3032"
    attr = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>'

    m = folium.Map(
        location=current_data["location"], 
        zoom_start=current_data["zoom"],
        tiles=tile_url,
        attr=attr,
        control_scale=True
    )

    marker_cluster = MarkerCluster(name="栖息地分布").add_to(m)

    for idx, point in enumerate(story_points):
        # 颜色逻辑：当前选中为红色，其他为蓝色
        color = "red" if idx == st.session_state.step else "cadetblue"
        
        # 处理图片用于弹窗 (需要Base64)
        img_b64 = get_img_as_base64(point['image_file'])
        img_html = f'<img src="data:image/jpeg;base64,{img_b64}" style="width: 100%; border-radius: 5px; margin-bottom: 8px;">' if img_b64 else ""

        popup_html = f"""
            <div style="width: 180px; text-align: center; font-family: sans-serif;">
                {img_html}
                <strong>{point['title']}</strong><br>
                <span style="font-size: 0.8em; color: gray;">{point['subtitle']}</span>
            </div>
        """
        popup = folium.Popup(popup_html, max_width=200)

        folium.Marker(
            location=point["location"],
            popup=popup,
            tooltip=f"{point['title']}",
            icon=folium.Icon(color=color, icon=point["icon"], prefix='fa', icon_color='white')
        ).add_to(marker_cluster)

    st_folium(m, height=650, width=None, use_container_width=True)

with col2:
    # --- 右侧：详细信息面板 ---
    
    # 标题区
    st.markdown(f"## {current_data['title']}")
    st.markdown(f"*{current_data['subtitle']}*")
    
    # 图片展示区
    if os.path.exists(current_data["image_file"]):
        st.image(current_data["image_file"], use_container_width=True)
    else:
        st.warning(f"图片未找到: {current_data['image_file']}，请确保图片在同一目录下。")
    
    # 文本内容区
    st.markdown("### Biography")
    st.write(current_data['bio'])
    
    st.markdown("### Location")
    st.write(current_data['habitat'])
    
    # 数据统计框
    st.markdown(f"""
    <div class="stat-box">
        <strong>📈 Population Change</strong><br>
        {current_data['population']}
    </div>
    """, unsafe_allow_html=True)
    
    # 濒危原因框
    st.markdown(f"""
    <div class="danger-box">
        <strong>⚠️ Why Endangered</strong><br>
        {current_data['danger']}
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")

    # 导航按钮
    b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
    with b_col1:
        if st.session_state.step > 0:
            st.button("⬅️ Previous", on_click=prev_step, use_container_width=True)
    with b_col3:
        if st.session_state.step < len(story_points) - 1:
            st.button("Next ➡️", on_click=next_step, type="primary", use_container_width=True)

    # 底部进度条
    progress = (st.session_state.step + 1) / len(story_points)
    st.progress(progress)
    st.caption(f"Species: {st.session_state.step + 1} / {len(story_points)}")