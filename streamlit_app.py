import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import base64
import os
from PIL import Image
from io import BytesIO

# --- 1. 工具函数 ---
def get_img_as_base64(file_path, width=None):
    """读取本地图片，压缩并转为Base64"""
    if not os.path.exists(file_path):
        return ""
    try:
        img = Image.open(file_path)
        if width:
            w_percent = (width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((width, h_size))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        return ""

# --- 2. 页面配置 ---
st.set_page_config(layout="wide", page_title="Endangered Animals of China")

# CSS样式优化：移除灰色代码块背景，美化字体
st.markdown("""
<style>
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    .story-card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #ff4b4b;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-family: sans-serif;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    .cn-text {
        color: #444;
        font-size: 0.95em;
        margin-top: 8px;
        display: block;
        font-weight: 500;
    }
    /* 强制去除st.markdown可能产生的默认code样式 */
    div.stMarkdown code {
        background-color: transparent;
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 准备数据 (已修复路径为 icon/ 并清理缩进) ---
story_points = [
    {
        "title": "Giant Panda (大熊猫)",
        "subtitle": "Ailuropoda melanoleuca",
        "image_file": "panda.jpg",
        "icon_path": "icon/大熊猫.png",  # 注意这里改成了 icon
        "location": [30.8, 103.0], 
        "zoom": 7,
        "bio": 'The Giant Panda is a medium-sized bear with distinctive black-and-white markings. They eat almost exclusively bamboo.<br><span class="cn-text">大熊猫是拥有独特黑白花纹的中型熊类。虽然拥有食肉动物的消化系统，但它们99%的食物是竹子，每天需进食26-84磅。</span>',
        "habitat": 'Temperate mountain forests in Sichuan, Shaanxi, and Gansu provinces.<br><span class="cn-text">四川、陕西、甘肃的高山森林 (海拔1200-3400米)，特别是秦岭和岷山山脉。</span>',
        "population": '2005: 1,596 → 2023: 1,900 (+19%)<br><strong>Trend: INCREASING (增长中) ✓</strong>',
        "danger": 'Habitat fragmentation and extreme dependence on bamboo.<br><span class="cn-text">基础设施导致的栖息地破碎化，对竹子的极度依赖，低繁殖率，以及气候变化威胁竹林生长。</span>'
    },
    {
        "title": "Yangtze Finless Porpoise (长江江豚)",
        "subtitle": "Neophocaena asiaeorientalis",
        "image_file": "jiangtun.jpg",
        "icon_path": "icon/江豚.png",
        "location": [29.5, 116.0],
        "zoom": 7,
        "bio": 'The world\'s only freshwater porpoise. They lack a dorsal fin and have a rounded head with a perpetual "smile."<br><span class="cn-text">世界上唯一的淡水鼠海豚，没有背鳍，头部圆润，看起来像在微笑。智商极高且群居。</span>',
        "habitat": 'Yangtze River, Poyang Lake, and Dongting Lake.<br><span class="cn-text">长江中下游干流及鄱阳湖、洞庭湖。喜欢水流缓慢、鱼类丰富的深水区。</span>',
        "population": '2006: 1,800 → 2022: 1,249 (-31%)<br><strong>Trend: RECOVERING (止跌回升) ↗</strong>',
        "danger": 'Fishing nets, vessel strikes, and water pollution.<br><span class="cn-text">渔网误捕，船只撞击，水利工程影响，水污染，以及非法采砂破坏栖息地。</span>'
    },
    {
        "title": "South China Tiger (华南虎)",
        "subtitle": "Panthera tigris amoyensis",
        "image_file": "dongbeihu.jpg", 
        "icon_path": "icon/老虎.png",
        "location": [27.0, 116.0], 
        "zoom": 6,
        "bio": 'The most critically endangered tiger subspecies. Now functionally extinct in the wild.<br><span class="cn-text">最濒危的老虎亚种。曾经是控制猎物数量的顶级掠食者，现在野外已无确切踪迹，仅剩圈养个体。</span>',
        "habitat": 'Historically in Hunan, Guangdong, Fujian. No viable wild population today.<br><span class="cn-text">历史上分布于湖南、广东、福建、江西的山地森林。现无野外种群。</span>',
        "population": 'Wild: 0 (Since 1990s)<br><strong>Trend: FUNCTIONALLY EXTINCT (野外功能性灭绝) ×</strong>',
        "danger": 'Historical hunting campaigns and massive habitat loss.<br><span class="cn-text">历史上的过度捕杀，栖息地大规模丧失(90%+)，猎物枯竭，以及近亲繁殖导致的严重基因瓶颈。</span>'
    },
    {
        "title": "Golden Snub-nosed Monkey (川金丝猴)",
        "subtitle": "Rhinopithecus roxellana",
        "image_file": "jinsihou.jpg",
        "icon_path": "icon/猴.png",
        "location": [33.5, 108.0],
        "zoom": 7,
        "bio": 'Named for their upturned nose and golden fur. They live in large social bands.<br><span class="cn-text">因朝天鼻和金色毛发得名，能忍受-10°C的低温。它们是群居动物，有时会形成200-600只的大群。</span>',
        "habitat": 'High-altitude forests in Sichuan, Shaanxi, and Hubei.<br><span class="cn-text">四川、陕西、甘肃、湖北的高山森林 (海拔1500-3400米)，特别是秦岭区域。</span>',
        "population": '2005: 15,000 → 2023: 23,000 (+53%)<br><strong>Trend: INCREASING (增长中) ↗</strong>',
        "danger": 'Habitat fragmentation and tourism disturbance.<br><span class="cn-text">道路和水坝导致的栖息地破碎化，非法伐木，气候变化导致栖息地向高处迁移，以及旅游干扰。</span>'
    },
    {
        "title": "Crested Ibis (朱鹮)",
        "subtitle": "Nipponia nippon",
        "image_file": "zhuxuan.jpg",
        "icon_path": "icon/鸟.png",
        "location": [33.3, 107.5], 
        "zoom": 8,
        "bio": 'A white wading bird with red facial skin. Rediscovered in 1981 with only 7 birds remaining.<br><span class="cn-text">拥有红色的面部皮肤和优雅的冠羽。曾被认为已灭绝，1981年仅在陕西洋县发现7只。</span>',
        "habitat": 'Rice paddies and wetlands in Shaanxi, Henan, and Zhejiang.<br><span class="cn-text">陕西、河南、浙江的稻田、湿地和森林混合区。需要高大的树木筑巢。</span>',
        "population": '1981: 7 → 2023: 5,000 (+71,329%)<br><strong>Trend: DRAMATIC RECOVERY (奇迹般恢复) ↑↑</strong>',
        "danger": 'Pesticide use and loss of wetland habitats.<br><span class="cn-text">极度严重的基因瓶颈，对农药非常敏感，以及农业开发导致的湿地和水生猎物减少。</span>'
    },
    {
        "title": "Snow Leopard (雪豹)",
        "subtitle": "Panthera uncia",
        "image_file": "xuebao.jpg",
        "icon_path": "icon/雪豹.png",
        "location": [34.5, 98.0],
        "zoom": 6,
        "bio": 'The "Ghost of the Mountains." Adapted to high altitudes with thick fur and massive paws.<br><span class="cn-text">高海拔的“雪山之王”，拥有厚实的毛皮和极长的尾巴。巨大的脚掌像雪鞋一样适应雪地行走。</span>',
        "habitat": 'Alpine zones in Tibet, Qinghai, and Xinjiang.<br><span class="cn-text">西藏、青海、新疆的高山裸岩地带 (海拔3000-5500米)，如三江源地区。</span>',
        "population": '2005: 2,000 → 2023: 2,400 (+20%)<br><strong>Trend: STABLE (稳中有升) →↗</strong>',
        "danger": 'Retaliatory killing, poaching, and climate change.<br><span class="cn-text">人兽冲突（报复性猎杀），非法盗猎，过度放牧导致的栖息地退化及气候变化。</span>'
    },
    {
        "title": "Chinese Alligator (扬子鳄)",
        "subtitle": "Alligator sinensis",
        "image_file": "yangzie.jpg",
        "icon_path": "icon/鳄鱼.png",
        "location": [30.9, 118.0],
        "zoom": 8,
        "bio": 'One of the smallest alligators. Hibernates in burrows during winter.<br><span class="cn-text">世界上体型最小的鳄鱼之一，性情相对温顺。冬季（11月-3月）会在洞穴中冬眠。</span>',
        "habitat": 'Slow-moving freshwater in Anhui and Zhejiang.<br><span class="cn-text">安徽、浙江的长江下游缓流淡水区（池塘、稻田）。</span>',
        "population": 'Wild: ~200 | Captive: ~15,000<br><strong>Trend: SLOWLY INCREASING (缓慢增长) ↗</strong>',
        "danger": 'Habitat loss to agriculture and pollution.<br><span class="cn-text">95%以上的栖息地因农业开发丧失，水污染，以及冬眠洞穴被破坏。</span>'
    },
    {
        "title": "Asian Elephant (亚洲象)",
        "subtitle": "Elephas maximus",
        "image_file": "yazhouxiang.jpg",
        "icon_path": "icon/大象.png",
        "location": [22.0, 100.8],
        "zoom": 8,
        "bio": 'China\'s largest land mammal. Highly intelligent and social.<br><span class="cn-text">中国最大的陆生哺乳动物。高度群居，由雌性首领带领。它们是维持森林生态系统的关键物种。</span>',
        "habitat": 'Tropical rainforests in southern Yunnan (Xishuangbanna).<br><span class="cn-text">云南南部（西双版纳、普洱）的热带/亚热带雨林。</span>',
        "population": '2005: 250 → 2023: 300 (+20%)<br><strong>Trend: STABLE (增长后趋稳) ↗→</strong>',
        "danger": 'Human-elephant conflict and habitat fragmentation.<br><span class="cn-text">极其有限的栖息地（<3000平方公里），剧烈的人象冲突（吃庄稼），以及基因交流受阻。</span>'
    },
    {
        "title": "Tibetan Antelope (藏羚羊)",
        "subtitle": "Pantholops hodgsonii",
        "image_file": "zanglingyang.jpg",
        "icon_path": "icon/鹿.png", 
        "location": [35.0, 89.0],
        "zoom": 6,
        "bio": 'Known for magnificent horns and fine wool. They undertake massive annual migrations.<br><span class="cn-text">青藏高原的标志性物种。以每年长距离迁徙产仔而闻名，奔跑速度可达80km/h。</span>',
        "habitat": 'Alpine meadows in Qinghai, Tibet, and Xinjiang.<br><span class="cn-text">青海、西藏、新疆的高寒草原 (海拔3700-5500米)，如可可西里自然保护区。</span>',
        "population": '2005: 75k → 2023: 200k (+167%)<br><strong>Trend: RECOVERED (显著恢复) ↑↑</strong>',
        "danger": 'Historical poaching and infrastructure blocking migration.<br><span class="cn-text">历史上因“沙图什”披肩导致的疯狂盗猎，现在面临铁路阻断迁徙路线及气候变化的威胁。</span>'
    },
    {
        "title": "Hainan Gibbon (海南长臂猿)",
        "subtitle": "Nomascus hainanus",
        "image_file": "changbiyuan.jpg",
        "icon_path": "icon/猩猩.png", 
        "location": [19.1, 109.1],
        "zoom": 9,
        "bio": 'The world\'s rarest primate. Known for their haunting songs.<br><span class="cn-text">世界上最稀有的灵长类动物。完全树栖，通过独特的歌声来沟通领地。实行一夫一妻制。</span>',
        "habitat": 'Tropical rainforests in Bawangling Reserve, Hainan Island.<br><span class="cn-text">仅存于海南岛霸王岭国家级自然保护区的热带雨林。</span>',
        "population": '1980s: <10 → 2023: 37<br><strong>Trend: CRITICAL BUT RECOVERING (极危但缓慢恢复) ↗</strong>',
        "danger": 'Catastrophic habitat loss and small population.<br><span class="cn-text">毁灭性的栖息地丧失（99%雨林被毁），种群极小导致抗灾难能力差，基因多样性匮乏。</span>'
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

# --- 5. 页面布局 ---
st.title("🇨🇳 Endangered Animals of China | 中国濒危动物分布")
col1, col2 = st.columns([2, 1.2], gap="medium")

# 获取当前需要展示的动物数据
current_data = story_points[st.session_state.step]

with col1:
    # --- 左侧：地图 ---
    tile_url = "https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}@2x.png?api_key=6e0e8bbd-0a37-467c-b601-d28e409c3032"
    attr = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>'

    # 这里的 center 设置为当前选中动物的坐标，这样地图会跟着动
    m = folium.Map(
        location=current_data["location"], 
        zoom_start=current_data["zoom"],
        tiles=tile_url,
        attr=attr,
        control_scale=True
    )

    marker_cluster = MarkerCluster(name="Locations").add_to(m)

    for idx, point in enumerate(story_points):
        is_active = (idx == st.session_state.step)
        
        # 放大当前选中的图标
        icon_display_size = (65, 65) if is_active else (40, 40)
        
        # 处理自定义图标
        icon_obj = None
        if os.path.exists(point["icon_path"]):
            icon_b64 = get_img_as_base64(point["icon_path"], width=65) # 稍微压一点
            if icon_b64:
                icon_src = f"data:image/png;base64,{icon_b64}"
                icon_obj = folium.CustomIcon(
                    icon_image=icon_src,
                    icon_size=icon_display_size,
                    icon_anchor=(icon_display_size[0]//2, icon_display_size[1]//2),
                    popup_anchor=(0, -icon_display_size[1]//2)
                )

        if not icon_obj:
            icon_obj = folium.Icon(color="red" if is_active else "blue", icon="info-sign")

        # 处理弹窗图片
        img_b64 = get_img_as_base64(point['image_file'], width=200)
        img_html = f'<img src="data:image/jpeg;base64,{img_b64}" style="width: 100%; border-radius: 5px; margin-bottom: 8px;">' if img_b64 else ""
        
        popup_content = f"""
        <div style="font-family:sans-serif; text-align:center; min-width:150px;">
            {img_html}
            <h4 style="margin:5px 0;">{point['title']}</h4>
        </div>
        """

        folium.Marker(
            location=point["location"],
            popup=folium.Popup(popup_content, max_width=250),
            tooltip=f"Click: {point['title']}",
            icon=icon_obj
        ).add_to(marker_cluster)

    # --- 核心修改：捕捉地图点击事件 ---
    map_data = st_folium(m, height=700, width=None, use_container_width=True)

    # 逻辑：如果用户点击了地图上的标记，我们查找是哪个动物，并更新状态
    if map_data and map_data.get("last_object_clicked"):
        clicked_lat = map_data["last_object_clicked"]["lat"]
        clicked_lng = map_data["last_object_clicked"]["lng"]
        
        # 遍历数据，找到坐标匹配的动物
        for i, p in enumerate(story_points):
            # 简单的浮点数近似比较
            if abs(p["location"][0] - clicked_lat) < 0.001 and abs(p["location"][1] - clicked_lng) < 0.001:
                if st.session_state.step != i:
                    st.session_state.step = i
                    st.rerun() # 强制刷新页面以更新右侧内容

with col2:
    # --- 右侧：详细信息面板 ---
    st.markdown(f"## {current_data['title']}")
    st.markdown(f"*{current_data['subtitle']}*")
    
    if os.path.exists(current_data["image_file"]):
        st.image(current_data["image_file"], use_container_width=True)
    else:
        st.warning(f"Image not found: {current_data['image_file']}")
    
    # 使用 markdown 的 html 渲染功能，配合上面的 CSS
    st.markdown("### 📖 Biography (物种简介)")
    st.markdown(f"<div class='story-card'>{current_data['bio']}</div>", unsafe_allow_html=True)
    
    st.markdown("### 📍 Location (栖息地)")
    st.markdown(f"<div class='story-card'>{current_data['habitat']}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="story-card" style="border-left-color: #2196F3; background-color: #e3f2fd;">
        <strong>📈 Population Status (种群现状)</strong><br><br>
        {current_data['population']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="story-card" style="border-left-color: #f44336; background-color: #ffebee;">
        <strong>⚠️ Threats (濒危原因)</strong><br><br>
        {current_data['danger']}
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")

    col_prev, col_space, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.session_state.step > 0:
            st.button("⬅️ Previous", on_click=prev_step, use_container_width=True)
            
    with col_next:
        if st.session_state.step < len(story_points) - 1:
            st.button("Next ➡️", on_click=next_step, type="primary", use_container_width=True)

    current_idx = st.session_state.step + 1
    total = len(story_points)
    st.caption(f"Viewing Species: {current_idx} / {total}")
    st.progress(current_idx / total)