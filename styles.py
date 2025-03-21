# задаем стили для объектов

import re
from IPython.display import display, HTML


BPMN_WIDTH = "820"
GEOMETRY_DEF = "y=20;width=120;height=60;label="; 


class Style:
    # Block styles
    BLUE 	= 'rounded=1;arcSize=11;whiteSpace=wrap;html=1;fillColor=#3B8AE6;fontColor=light-dark(#ffffff, #ededed);strokeColor=none;'
    MAROON 	= 'rounded=1;arcSize=11;whiteSpace=wrap;html=1;fillColor=#800000;fontColor=light-dark(#ffffff, #ededed);strokeColor=none;'
    GRAY   	= 'rounded=1;arcSize=11;whiteSpace=wrap;html=1;fillColor=#999999;fontColor=light-dark(#ffffff, #ededed);strokeColor=none;'
    CHERRY 	= 'rounded=1;arcSize=11;whiteSpace=wrap;html=1;fillColor=#b11e42;fontColor=light-dark(#ffffff, #ededed);strokeColor=none;'
    BLACK 	= 'rounded=1;arcSize=7;whiteSpace=wrap;html=1;fillColor=#000000;fontColor=light-dark(#ffffff, #ededed);strokeColor=none;'
    DEF 	= 'rounded=1;arcSize=11;whiteSpace=wrap;html=1;'
    LABEL 	= "rounded=1;arcSize=5;whiteSpace=wrap;html=1;strokeColor=none;align=center;verticalAlign=middle;fontFamily=Helvetica;fontSize=12;fontColor=#FFFFFF;fillColor=#4D4D9D"

    # Line styles
    LINE_DOTTED = "rounded=0jettySize=auto;html=1;dashed=1;dashPattern=8 8;startArrow=none;startFill=0;strokeColor=#555555;"
    LINE_LES 	= "rounded=0jettySize=auto;html=1;dashed=1;dashPattern=2 2;startArrow=none;startFill=0;strokeColor=#b11e42;"
    LINE_DEF  	= "strokeColor=#222222;"
    LINE_BUS  	= "strokeColor=#222222;edgeStyle=elbowEdgeStyle"
    LINE_TEXT	= "whiteSpace=wrap;html=1;strokeColor=#555555;align=center;verticalAlign=middle;fontFamily=Helvetica;fontSize=10;fontColor=#555555;labelBackgroundColor=default;fontStyle=2"

    def __str__(self):
        return self._get_styles_as_string()

    def __repr__(self):
        return self._get_styles_as_string()

    def _get_styles_as_string(self):
        result = "Стили класса Style:\n"
        for attr in dir(self):
            if not attr.startswith("__") and not callable(getattr(self, attr)):
                result += f"{attr}: {getattr(self, attr)}\n"
        return result.strip()

    def _extract_color(self, style_str, key, default="#000000"):
        """Извлекает цвет по ключу: fillColor, fontColor, strokeColor"""
        pattern = rf"{key}=([^;]+)"
        match = re.search(pattern, style_str)
        if match:
            value = match.group(1)
            if value == "none":
                return "transparent"
            if value.startswith("light-dark("):
                return value.split("(")[1].split(",")[0].strip()
            return value
        return default

    def _extract_dash_pattern(self, style_str):
        """Извлекает dashPattern для линий, если оно есть"""
        pattern = r"dashPattern=([\d ]+)"
        match = re.search(pattern, style_str)
        if match:
            return match.group(1)
        return None

    def to_html_table(self):
        block_rows, line_rows = "", ""
        for attr in dir(self):
            if attr.startswith("__") or callable(getattr(self, attr)):
                continue

            style_str = getattr(self, attr)
            fill = self._extract_color(style_str, "fillColor", "#FFFFFF")
            font = self._extract_color(style_str, "fontColor", "#000000")
            stroke = self._extract_color(style_str, "strokeColor", "#000000")
            dash_pattern = self._extract_dash_pattern(style_str)

            # Блочный стиль — визуализация как прямоугольник
            block_cell_style = f"background:{fill}; color:{font}; padding:5px; border-radius:5px; border:2px solid {stroke};"
            block_preview = f'<div style="{block_cell_style}">{attr}</div>'

            # Линия — отрисовка line с dashPattern и цветом
            line_preview = f'<div style="height:2px; background:{stroke}; margin:4px 0;'
            if dash_pattern:
                dash_values = dash_pattern.split()
                line_preview += f'background-image: repeating-linear-gradient(to right, {stroke}, {stroke} {dash_values[0]}px, transparent {dash_values[0]}px, transparent {dash_values[1]}px);'
            line_preview += '"></div>'

            # Добавляем в соответствующий столбец
            if "edgeStyle" in style_str or "strokeColor" in style_str and "fillColor" not in style_str:
                # Линейный стиль
                line_rows += f"""
                    <tr>
                        <td><b>{attr}</b></td>
                        <td>{line_preview}</td>
                        <td style="font-family:monospace; font-size:11px;">{style_str}</td>
                        <td>{stroke}</td>
                        <td>{dash_pattern if dash_pattern else "solid"}</td>
                    </tr>
                """
            else:
                # Блочный стиль
                block_rows += f"""
                    <tr>
                        <td><b>{attr}</b></td>
                        <td>{block_preview}</td>
                        <td style="font-family:monospace; font-size:11px;">{style_str}</td>
                        <td>{fill}</td>
                        <td>{stroke}</td>
                    </tr>
                """

        html = f"""
            <h3>All Styles</h3>
            <table border="1" cellspacing="0" cellpadding="4" style="border-collapse:collapse; font-family:sans-serif; font-size:13px;">
                <tr style="background:#f0f0f0;">
                    <th>Style Name</th>
                    <th>Preview</th>
                    <th>Style String</th>
                    <th>Fill Color</th>
                    <th>Stroke Color</th>
                    <th>Dash Pattern</th>
                </tr>
                {block_rows}
                {line_rows}
            </table>
        """
        display(HTML(html))

