import streamlit as st
import folium
from streamlit_folium import st_folium
# 导入聚类插件，让地图更整洁
from folium.plugins import MarkerCluster

# --- 1. 页面基础设置 ---
st.set_page_config(layout="wide", page_title="中国濒危动物 StoryMap")

st.markdown("""
<style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    h1 {margin-top: 0;}
    /* 美化右侧故事卡的样式 */
    .story-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* 调整地图容器的样式 */
    iframe {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 准备数据 ---
story_points = [
    {
        "title": "开始探索：中国濒危动物",
        "description": "中国幅员辽阔，拥有众多珍稀野生动物。让我们沿着地图，探索它们的栖息地。",
        "location": [35.8617, 104.1954],
        "zoom": 4,
        "image": "https://images.unsplash.com/photo-1535338454770-8be927b5a00b?auto=format&fit=crop&w=800&q=80",
        "icon": "home"
    },
    {
        "title": "大熊猫 (Giant Panda)",
        "description": "栖息地：四川、陕西、甘肃的山区。\n\n大熊猫是中国特有的珍稀动物，以竹子为食。",
        "location": [30.8, 103.0],
        "zoom": 7,
        "image": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?auto=format&fit=crop&w=800&q=80",
        "icon": "paw"
    },
    {
        "title": "金丝猴 (Golden Snub-nosed Monkey)",
        "description": "栖息地：秦岭、神农架等高山密林。\n\n它们拥有美丽的金色毛发和独特的蓝色面孔。",
        "location": [33.5, 108.0],
        "zoom": 7,
        "image": "https://images.unsplash.com/photo-1548681528-6a5c45b66b42?auto=format&fit=crop&w=800&q=80",
        "icon": "tree"
    },
    {
        "title": "东北虎 (Siberian Tiger)",
        "description": "栖息地：中国东北及俄罗斯远东地区。\n\n世界上最大的猫科动物之一，森林之王。",
        "location": [45.0, 130.0],
        "zoom": 6,
        "image": "https://images.unsplash.com/photo-1501705388883-4ed8a543392c?auto=format&fit=crop&w=800&q=80",
        "icon": "star"
    }
]

# --- 3. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.step = 0

def next_step():
    if st.session_state.step < len(story_points) - 1:
        st.session_state.step += 1

def prev_step():
    if st.session_state.step > 0:
        st.session_state.step -= 1

current_data = story_points[st.session_state.step]

# --- 4. 页面布局 ---
col1, col2 = st.columns([2, 1], gap="medium")

with col1:
    # --- 左侧：美化后的地图 ---
    
    # 1. 创建地图底图，使用你提供的 URL 和 API Key
    # 注意：必须添加 attr (版权声明)，这是使用第三方地图的规范
    tile_url = "https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}@2x.png?api_key=6e0e8bbd-0a37-467c-b601-d28e409c3032"
    tile_attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'

    m = folium.Map(
        location=current_data["location"], 
        zoom_start=current_data["zoom"],
        tiles=tile_url,
        attr=tile_attribution,
        control_scale=True # 添加比例尺
    )

    # 2. 创建一个聚类组，把所有点都放进去，实现自动聚合效果
    marker_cluster = MarkerCluster(name="栖息地分布").add_to(m)

    # 在地图上添加所有点的标记
    for idx, point in enumerate(story_points):
        # 视觉对比：当前点用红色，其他点用低调的灰蓝色
        color = "red" if idx == st.session_state.step else "cadetblue"
        icon_type = point["icon"]
        
        # 创建一个漂亮的 HTML 弹窗 (Popup)，包含小图和标题
        popup_html = f"""
            <div style="width: 150px; text-align: center;">
                <img src="{point['image']}" style="width: 100%; border-radius: 5px; margin-bottom: 8px;">
                <strong>{point['title']}</strong>
            </div>
        """
        popup = folium.Popup(popup_html, max_width=200)

        # 创建标记并加入到聚类组中
        folium.Marker(
            location=point["location"],
            popup=popup,
            tooltip=f"点击查看：{point['title']}", # 鼠标悬停提示
            icon=folium.Icon(color=color, icon=icon_type, prefix='fa', icon_color='white')
        ).add_to(marker_cluster)

    # 添加图层控制器，让用户可以开关聚类图层（显得更专业）
    folium.LayerControl().add_to(m)

    # 渲染地图，增加一点圆角和阴影效果（在CSS里定义）
    st_folium(m, height=600, width=None, use_container_width=True)

with col2:
    # --- 右侧：故事面板 (保持不变) ---
    st.markdown(f"## {current_data['title']}")
    
    # 给图片加个圆角
    st.markdown(
        f'<img src="{current_data["image"]}" style="width:100%; border-radius: 10px;">', 
        unsafe_allow_html=True
    )
    
    st.markdown(f"""
    <div class="story-card" style="margin-top: 20px;">
        {current_data['description']}
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")

    # --- 导航按钮 ---
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    
    with btn_col1:
        if st.session_state.step > 0:
            st.button("⬅️ 上一站", on_click=prev_step, use_container_width=True)
            
    with btn_col3:
        if st.session_state.step < len(story_points) - 1:
            st.button("下一站 ➡️", on_click=next_step, type="primary", use_container_width=True)

    st.caption(f"当前进度: {st.session_state.step + 1} / {len(story_points)}")