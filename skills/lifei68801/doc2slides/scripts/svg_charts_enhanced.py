#!/usr/bin/env python3
# Part of doc2slides skill.

#!/usr/bin/env python3
"""
专业 SVG 图表组件库
- 真实数据可视化
- 渐变装饰
- 多种图表类型
"""

def progress_ring(value: float, size: int = 100, color: str = "#F59E0B", label: str = "") -> str:
    """真实进度环"""
    import math
    radius = (size - 10) / 2
    circumference = 2 * math.pi * radius
    progress = value / 100 * circumference
    offset = circumference - progress
    
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <defs>
    <linearGradient id="grad_{value}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color};stop-opacity:0.6" />
    </linearGradient>
  </defs>
  <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="#1A2332" stroke-width="6"/>
  <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="url(#grad_{value})" stroke-width="6"
    stroke-linecap="round"
    stroke-dasharray="{circumference}"
    stroke-dashoffset="{offset}"
    transform="rotate(-90 {size/2} {size/2})"/>
  <text x="{size/2}" y="{size/2}" text-anchor="middle" fill="white" font-size="18" font-weight="bold" dy=".3em">{int(value)}%</text>
</svg>'''

def bar_chart(data: list, width: int = 500, height: int = 300, colors: list = None) -> str:
    """柱状图 - data: [{'label': str, 'value': float, 'unit': str}]"""
    if not colors:
        colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6", "#EC4899"]
    
    bars = []
    max_val = max(d['value'] for d in data) if data else 1
    bar_width = (width - 100) / len(data) - 20
    
    for i, item in enumerate(data):
        bar_height = (item['value'] / max_val) * (height - 80)
        x = 50 + i * (bar_width + 20)
        y = height - 50 - bar_height
        color = colors[i % len(colors)]
        
        bars.append(f'''
    <defs>
      <linearGradient id="bar_{i}" x1="0%" y1="100%" x2="0%" y2="0%">
        <stop offset="0%" style="stop-color:{color};stop-opacity:0.8" />
        <stop offset="100%" style="stop-color:{color};stop-opacity:1" />
      </linearGradient>
    </defs>
    <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" rx="8" fill="url(#bar_{i})"/>
    <text x="{x + bar_width/2}" y="{y - 10}" text-anchor="middle" fill="white" font-size="12" font-weight="bold">{item['value']}{item.get('unit', '')}</text>
    <text x="{x + bar_width/2}" y="{height - 25}" text-anchor="middle" fill="#94A3B8" font-size="11">{item['label']}</text>''')
    
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {''.join(bars)}
</svg>'''

def kpi_card_big(number: str, unit: str, label: str, color: str = "#F59E0B", icon: str = None) -> str:
    """大数字 KPI 卡片"""
    icon_svg = ""
    if icon:
        icon_svg = f'''<svg width="32" height="32" viewBox="0 0 24 24" style="position: absolute; top: 20px; right: 20px; opacity: 0.3;">
    <path fill="{color}" d="{icon}"/>
  </svg>'''
    
    return f'''<div style="background: #1A2332; border-radius: 16px; padding: 24px; border: 1px solid rgba(255,255,255,0.1); position: relative;">
  {icon_svg}
  <div style="font-size: 48px; font-weight: 800; color: {color};">{number}<span style="font-size: 20px;">{unit}</span></div>
  <div style="font-size: 14px; color: #94A3B8; margin-top: 8px;">{label}</div>
</div>'''

def comparison_card(left_title: str, left_points: list, left_color: str, 
                   right_title: str, right_points: list, right_color: str) -> str:
    """左右对比卡片"""
    left_items = '\n'.join([f'''<div style="display: flex; align-items: start; gap: 12px;">
      <div style="width: 8px; height: 8px; background: {left_color}; border-radius: 50%; margin-top: 6px; flex-shrink: 0;"></div>
      <div style="font-size: 15px; color: #E5E7EB;">{point}</div>
    </div>''' for point in left_points])
    
    right_items = '\n'.join([f'''<div style="display: flex; align-items: start; gap: 12px;">
      <div style="width: 8px; height: 8px; background: {right_color}; border-radius: 50%; margin-top: 6px; flex-shrink: 0;"></div>
      <div style="font-size: 15px; color: #E5E7EB;">{point}</div>
    </div>''' for point in right_points])
    
    return f'''<div style="display: flex; gap: 40px;">
  <div style="flex: 1; background: #1A2332; border-radius: 16px; padding: 32px; border-top: 4px solid {left_color};">
    <h3 style="font-size: 24px; color: {left_color}; margin: 0 0 24px 0;">{left_title}</h3>
    <div style="display: flex; flex-direction: column; gap: 16px;">
      {left_items}
    </div>
  </div>
  
  <div style="display: flex; align-items: center;">
    <div style="width: 60px; height: 60px; border-radius: 50%; background: #1A2332; border: 3px solid #374151; display: flex; align-items: center; justify-content: center;">
      <span style="font-size: 20px; font-weight: bold; color: white;">VS</span>
    </div>
  </div>
  
  <div style="flex: 1; background: #1A2332; border-radius: 16px; padding: 32px; border-top: 4px solid {right_color};">
    <h3 style="font-size: 24px; color: {right_color}; margin: 0 0 24px 0;">{right_title}</h3>
    <div style="display: flex; flex-direction: column; gap: 16px;">
      {right_items}
    </div>
  </div>
</div>'''

def pyramid_with_cards(layers: list, card_color: str = "#F59E0B") -> str:
    """金字塔 + 右侧卡片
    layers: [{'title': str, 'desc': str, 'color': str}]
    """
    colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6"]
    
    # 金字塔 SVG
    pyramid_parts = []
    for i, layer in enumerate(layers):
        # 从上到下，宽度逐渐增加
        top_y = 30 + i * 90
        bottom_y = top_y + 60
        top_width = 80 + i * 60
        bottom_width = 140 + i * 60
        
        pyramid_parts.append(f'''<path d="M 200 {top_y} L {200 + top_width/2} {bottom_y} L {200 - top_width/2} {bottom_y} Z" fill="{layer.get('color', colors[i % len(colors)])}"/>''')
        pyramid_parts.append(f'''<text x="200" y="{(top_y + bottom_y)/2}" text-anchor="middle" fill="white" font-size="16" font-weight="bold">{i+1}</text>''')
    
    pyramid_svg = f'''<svg width="400" height="400" viewBox="0 0 400 400">
  {''.join(pyramid_parts)}
</svg>'''
    
    # 右侧卡片
    cards = []
    for i, layer in enumerate(layers):
        color = layer.get('color', colors[i % len(colors)])
        cards.append(f'''<div style="background: #1A2332; border-radius: 12px; padding: 20px; border-left: 4px solid {color};">
      <div style="font-size: 16px; font-weight: bold; color: white;">{layer['title']}</div>
      <div style="font-size: 13px; color: #94A3B8; margin-top: 8px;">{layer['desc']}</div>
    </div>''')
    
    return f'''<div style="display: flex; gap: 40px; align-items: start;">
  <div style="flex-shrink: 0;">
    {pyramid_svg}
  </div>
  <div style="flex: 1; display: flex; flex-direction: column; gap: 16px;">
    {''.join(cards)}
  </div>
</div>'''

def timeline_horizontal(events: list, width: int = 1100, height: int = 200) -> str:
    """横向时间线
    events: [{'year': str, 'title': str, 'desc': str}]
    """
    if not events:
        return ""
    
    spacing = (width - 100) / (len(events) - 1) if len(events) > 1 else 0
    colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6"]
    
    # 时间线主线
    timeline = [f'<line x1="50" y1="60" x2="{width-50}" y2="60" stroke="#374151" stroke-width="3"/>']
    
    # 事件节点
    for i, event in enumerate(events):
        x = 50 + i * spacing
        color = colors[i % len(colors)]
        
        timeline.append(f'''
    <circle cx="{x}" cy="60" r="15" fill="{color}"/>
    <text x="{x}" y="65" text-anchor="middle" fill="white" font-size="12" font-weight="bold">{event['year']}</text>
    <text x="{x}" y="100" text-anchor="middle" fill="white" font-size="14" font-weight="bold">{event['title']}</text>
    <text x="{x}" y="120" text-anchor="middle" fill="#94A3B8" font-size="11">{event.get('desc', '')}</text>''')
    
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {''.join(timeline)}
</svg>'''

def decorative_elements() -> str:
    """装饰性背景元素"""
    return '''
  <!-- 背景网格 -->
  <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.03; pointer-events: none;">
    <defs>
      <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
        <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#4B5563" stroke-width="0.5"/>
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#grid)"/>
  </svg>
  
  <!-- 渐变圆形装饰 -->
  <svg style="position: absolute; top: -100px; right: -100px; width: 400px; height: 400px; pointer-events: none;">
    <defs>
      <radialGradient id="glow">
        <stop offset="0%" style="stop-color:#F59E0B;stop-opacity:0.15" />
        <stop offset="100%" style="stop-color:#F59E0B;stop-opacity:0" />
      </radialGradient>
    </defs>
    <circle cx="200" cy="200" r="200" fill="url(#glow)"/>
  </svg>
'''

def pie_chart(data: list, size: int = 300, center_text: str = None) -> str:
    """饼图/环形图 - data: [{'label': str, 'value': float, 'color': str}]
    
    使用 SVG arc 路径绘制饼图，支持中心文字（环形图模式）
    """
    if not data:
        return ""
    
    import math
    
    # 默认配色
    default_colors = ["#F59E0B", "#EA580C", "#10B981", "#3B82F6", "#8B5CF6", "#EC4899"]
    
    # 计算总和
    total = sum(d['value'] for d in data)
    if total == 0:
        total = 1
    
    # 圆心坐标
    cx, cy = size / 2, size / 2
    radius = size / 2 - 20
    
    # 内圆半径（环形图模式）
    inner_radius = radius * 0.6 if center_text else 0
    
    # 计算每个扇形的角度
    paths = []
    start_angle = -90  # 从12点钟方向开始
    
    for i, item in enumerate(data):
        color = item.get('color', default_colors[i % len(default_colors)])
        value = item['value']
        angle = (value / total) * 360
        
        # 计算扇形路径
        end_angle = start_angle + angle
        
        # 转换为弧度
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # 计算外圆弧的起止点
        x1 = cx + radius * math.cos(start_rad)
        y1 = cy + radius * math.sin(start_rad)
        x2 = cx + radius * math.cos(end_rad)
        y2 = cy + radius * math.sin(end_rad)
        
        # 判断是否为大角度弧
        large_arc = 1 if angle > 180 else 0
        
        if inner_radius > 0:
            # 环形图：计算内圆弧
            ix1 = cx + inner_radius * math.cos(end_rad)
            iy1 = cy + inner_radius * math.sin(end_rad)
            ix2 = cx + inner_radius * math.cos(start_rad)
            iy2 = cy + inner_radius * math.sin(start_rad)
            
            # 环形路径：外弧 -> 内弧（反向）
            path = f'''<path d="M {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} L {ix1} {iy1} A {inner_radius} {inner_radius} 0 {large_arc} 0 {ix2} {iy2} Z" 
            fill="{color}" opacity="0.9">
            <title>{item['label']}: {value} ({value/total*100:.1f}%)</title>
          </path>'''
        else:
            # 饼图：从圆心开始
            path = f'''<path d="M {cx} {cy} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z" 
            fill="{color}" opacity="0.9">
            <title>{item['label']}: {value} ({value/total*100:.1f}%)</title>
          </path>'''
        
        paths.append(path)
        start_angle = end_angle
    
    # 中心文字（环形图模式）
    center_svg = ""
    if center_text:
        center_svg = f'''<text x="{cx}" y="{cy}" text-anchor="middle" fill="white" font-size="24" font-weight="bold" dy=".3em">{center_text}</text>'''
    
    # 图例
    legends = []
    for i, item in enumerate(data):
        color = item.get('color', default_colors[i % len(default_colors)])
        legends.append(f'''<div style="display: flex; align-items: center; gap: 8px; margin-top: 8px;">
        <div style="width: 12px; height: 12px; background: {color}; border-radius: 2px;"></div>
        <span style="font-size: 13px; color: #94A3B8;">{item['label']}</span>
        <span style="font-size: 13px; color: white; font-weight: bold;">{item['value']}</span>
      </div>''')
    
    return f'''<div style="display: flex; gap: 40px; align-items: center;">
  <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
    {''.join(paths)}
    {center_svg}
  </svg>
  <div style="flex: 1;">
    {''.join(legends)}
  </div>
</div>'''


def radar_chart(data: list, size: int = 400, title: str = None) -> str:
    """雷达图 - data: [{'label': str, 'value': float, 'max': float}]
    
    多维度能力对比，自动绘制网格和数值区域
    """
    if not data or len(data) < 3:
        return ""
    
    import math
    
    n = len(data)
    cx, cy = size / 2, size / 2
    radius = size / 2 - 60
    
    # 计算每个维度的角度
    angle_step = 360 / n
    
    # 绘制网格（3层）
    grid_levels = [0.33, 0.66, 1.0]
    grid_paths = []
    
    for level in grid_levels:
        points = []
        for i in range(n):
            angle = math.radians(i * angle_step - 90)
            r = radius * level
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append(f"{x:.1f},{y:.1f}")
        
        grid_paths.append(f'<polygon points="{" ".join(points)}" fill="none" stroke="#374151" stroke-width="1" opacity="0.5"/>')
    
    # 绘制轴线
    axis_lines = []
    for i in range(n):
        angle = math.radians(i * angle_step - 90)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        axis_lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#374151" stroke-width="1" opacity="0.3"/>')
    
    # 绘制数据区域
    data_points = []
    for i, item in enumerate(data):
        max_val = item.get('max', 100)
        value = min(item['value'], max_val)  # 不超过最大值
        ratio = value / max_val if max_val > 0 else 0
        
        angle = math.radians(i * angle_step - 90)
        r = radius * ratio
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        data_points.append(f"{x:.1f},{y:.1f}")
    
    data_area = f'<polygon points="{" ".join(data_points)}" fill="#F59E0B" fill-opacity="0.3" stroke="#F59E0B" stroke-width="2"/>'
    
    # 绘制数据点
    data_dots = []
    for i, item in enumerate(data):
        max_val = item.get('max', 100)
        value = min(item['value'], max_val)
        ratio = value / max_val if max_val > 0 else 0
        
        angle = math.radians(i * angle_step - 90)
        r = radius * ratio
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        data_dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#F59E0B"/>')
    
    # 绘制标签
    labels = []
    for i, item in enumerate(data):
        angle = math.radians(i * angle_step - 90)
        label_r = radius + 30
        x = cx + label_r * math.cos(angle)
        y = cy + label_r * math.sin(angle)
        labels.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" fill="#94A3B8" font-size="12">{item["label"]}</text>')
        
        # 数值标签
        value_r = radius * (item['value'] / item.get('max', 100)) + 15
        vx = cx + value_r * math.cos(angle)
        vy = cy + value_r * math.sin(angle)
        labels.append(f'<text x="{vx:.1f}" y="{vy:.1f}" text-anchor="middle" fill="white" font-size="11" font-weight="bold">{item["value"]}</text>')
    
    title_svg = f'<text x="{cx}" y="30" text-anchor="middle" fill="white" font-size="16" font-weight="bold">{title}</text>' if title else ""
    
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  {title_svg}
  {''.join(grid_paths)}
  {''.join(axis_lines)}
  {data_area}
  {''.join(data_dots)}
  {''.join(labels)}
</svg>'''


def data_table(headers: list, rows: list, column_widths: list = None) -> str:
    """数据表格 - 适合大量数据展示
    
    Args:
        headers: ['列1', '列2', '列3']
        rows: [['值1', '值2', '值3'], ...]
        column_widths: [200, 150, 150] (可选)
    """
    if not headers or not rows:
        return ""
    
    n_cols = len(headers)
    
    # 默认等宽
    if not column_widths:
        total_width = 800
        col_width = total_width // n_cols
        column_widths = [col_width] * n_cols
    
    # 表头
    header_cells = []
    for i, h in enumerate(headers):
        header_cells.append(f'''<th style="background: #1A2332; padding: 16px; text-align: left; font-size: 14px; font-weight: bold; color: #F59E0B; border-bottom: 2px solid #F59E0B;">
          {h}
        </th>''')
    
    # 表体
    body_rows = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            # 最后一列右对齐（通常是数值）
            align = "right" if i == n_cols - 1 else "left"
            cells.append(f'''<td style="padding: 14px 16px; font-size: 13px; color: white; border-bottom: 1px solid #374151; text-align: {align};">
              {cell}
            </td>''')
        
        body_rows.append(f'''<tr style="background: rgba(26, 35, 50, 0.5);">
          {''.join(cells)}
        </tr>''')
    
    return f'''<div style="background: #0B1221; border-radius: 12px; overflow: hidden; border: 1px solid #374151;">
  <table style="width: 100%; border-collapse: collapse;">
    <thead>
      <tr>
        {''.join(header_cells)}
      </tr>
    </thead>
    <tbody>
      {''.join(body_rows)}
    </tbody>
  </table>
</div>'''


def gauge_chart(value: float, max_value: float = 100, size: int = 200, 
                label: str = "", color: str = "#F59E0B") -> str:
    """仪表盘图表 - 半圆仪表
    
    适合展示进度、完成率等单一指标
    """
    import math
    
    cx, cy = size / 2, size * 0.65
    radius = size / 2 - 20
    
    # 计算角度（半圆：-180度到0度）
    ratio = min(value / max_value, 1.0) if max_value > 0 else 0
    angle = -180 + (ratio * 180)  # 从左边开始
    
    # 背景弧
    bg_arc = f'''<path d="M {cx - radius} {cy} A {radius} {radius} 0 0 1 {cx + radius} {cy}" 
      fill="none" stroke="#374151" stroke-width="12" stroke-linecap="round"/>'''
    
    # 数值弧
    end_rad = math.radians(angle)
    end_x = cx + radius * math.cos(end_rad)
    end_y = cy + radius * math.sin(end_rad)
    
    large_arc = 1 if ratio > 0.5 else 0
    value_arc = f'''<path d="M {cx - radius} {cy} A {radius} {radius} 0 {large_arc} 1 {end_x:.1f} {end_y:.1f}" 
      fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round"/>'''
    
    # 指针
    pointer_rad = math.radians(-180 + ratio * 180)
    pointer_len = radius * 0.7
    pointer_x = cx + pointer_len * math.cos(pointer_rad)
    pointer_y = cy + pointer_len * math.sin(pointer_rad)
    pointer = f'''<line x1="{cx}" y1="{cy}" x2="{pointer_x:.1f}" y2="{pointer_y:.1f}" 
      stroke="white" stroke-width="3" stroke-linecap="round"/>
      <circle cx="{cx}" cy="{cy}" r="8" fill="white"/>'''
    
    # 数值文字
    value_text = f'''<text x="{cx}" y="{cy + 50}" text-anchor="middle" fill="white" font-size="32" font-weight="bold">{int(value)}</text>'''
    label_text = f'''<text x="{cx}" y="{cy + 75}" text-anchor="middle" fill="#94A3B8" font-size="14">{label}</text>''' if label else ""
    
    return f'''<svg width="{size}" height="{size * 0.7}" viewBox="0 0 {size} {size * 0.7}">
  {bg_arc}
  {value_arc}
  {pointer}
  {value_text}
  {label_text}
</svg>'''


# 常用图标 SVG path
ICONS = {
    "users": "M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z",
    "chart": "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z",
    "dollar": "M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
    "check": "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
}
