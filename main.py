# 2025-03-21 This is a sample Python script.

import xml.etree.ElementTree as ET
import re
import argparse


import styles
Style = styles.Style()


GEOMETRY_DEF_STR = "y=20;width=120;height=60;label=;text=";


def parse_style_to_dict(style_string: str) -> dict:
    pattern = r'([^=;]+)=([^;]+)'
    matches = re.findall(pattern, style_string)
    attr_dict = {key.strip(): value.strip() for key, value in matches}
    return attr_dict


def dict_to_string(attr_dict: dict) -> str:
    return ";".join([f'{k}={v}' for k, v in attr_dict.items()]) + ";"


def parse_style(style_str):
    # Находит все пары ключ=значение, игнорируя пробелы и табуляции вокруг
    style_dict = dict(re.findall(r'\s*([^=;\s]+)\s*=\s*([^;]*)', style_str))

    # Добавление всех отсутствующих ключей с пустыми значениями (если есть)
    keys = re.findall(r'\s*([^=;\s]+)\s*=', style_str)
    for key in keys:
        if key not in style_dict:
            style_dict[key] = ''

    return style_dict


def merge_styles(styles):
    merged_dict = {}
    merged_flags = []

    for style in styles:
        for part in style.strip(';').split(';'):
            if '=' in part:
                k, v = part.split('=', 1)
                merged_dict[k] = v
            elif part:
                merged_flags.append(part)

    # Удаляем дублирующиеся флаги, сохраняем порядок
    merged_flags = list(dict.fromkeys(merged_flags))

    # Собираем финальную строку
    parts = merged_flags + [f'{k}={v}' for k, v in merged_dict.items()]
    return ';'.join(parts) + ';'


def create_cell(root, cell_id, value, style, geometry, parent, label_value=""):
    """Создание ячейки с блоком и подписью в нижнем углу."""

    # Основной блок (vertex)
    cell = ET.SubElement(root, "mxCell", id=cell_id, value=value, style=style, vertex="1", parent=parent)
    ET.SubElement(cell, "mxGeometry",
                  x=geometry.get("x", "0"),
                  y=geometry["y"],
                  width=geometry["width"],
                  height=geometry["height"],
                  **{"as": "geometry"})

    if label_value != "":
        # Подпись (label) — вложенная mxCell
        label_style = "whiteSpace=wrap;fontSize=9;fontStyle=0;fillColor=#222222;fontColor=light-dark(#ffffff, #ededed);strokeColor=none;"
        label_cell = ET.SubElement(root, "mxCell",
                                   id=f"label_{cell_id}",
                                   value=label_value,
                                   style=label_style,
                                   vertex="1", connectable="0", parent=cell_id)

        # Геометрия метки — снизу блока (например, высота метки 12px, смещение 2px)
        label_height = 12
        offset = 0
        label_x = 0  # по левому краю блока
        label_y = str(float(geometry["height"]) - label_height - offset)
        ET.SubElement(label_cell, "mxGeometry",
                      x=str(label_x),
                      y=str(label_y),
                      width="50",  # geometry["width"],
                      height=str(label_height),
                      **{"as": "geometry"})

    return cell


def generate_lane(root, lane_id, lane_info):
    """Генерация лэйна с блоками."""

    LANE_STYLE_DEF = "swimlane;html=1;startSize=40;horizontal=0"

    lane_params = merge_styles(
        [LANE_STYLE_DEF, lane_info['lane_params']]) if 'lane_params' in lane_info else LANE_STYLE_DEF

    lane_cell = ET.SubElement(root, "mxCell", id=lane_id, value=lane_id, style=lane_params, vertex="1", parent="header")

    lane_geom = parse_style(lane_info["geometry"])

    ET.SubElement(lane_cell, "mxGeometry", y=lane_geom["y"],
                  width=lane_geom["width"],
                  height=lane_geom["height"], **{"as": "geometry"})

    for block_id, block_param in lane_info["blocks"].items():
        # генерацпия блоков

        lane_block_param = lane_info["block_params"] if "block_params" in lane_info else ""

        block_param_merged = merge_styles([Style.DEF, GEOMETRY_DEF_STR, lane_block_param, block_param])

        print(f'''* {lane_id:<15}:{block_id:<25}:{block_param_merged}"''')

        param = parse_style(block_param_merged)

        create_cell(root, block_id, block_id + param["text"], block_param_merged,
                    {"x": param["x"],
                     "y": param["y"],
                     "width": param["width"],
                     "height": param["height"]},
                    lane_id, param["label"])


def generate_connections(root, connections):
    """Создание связей между блоками с автоматическим генерированием id."""
    for index, conn in enumerate(connections, start=1):
        conn_id = f"link_{index}"

        _style = conn[3] if conn[3] else "whiteSpace=wrap;rounded=0;jettySize=auto;html=1;"

        conn_cell = ET.SubElement(root, "mxCell", id=conn_id,
                                  style=_style,
                                  edge="1", source=conn[0], target=conn[1], parent="1")
        ET.SubElement(conn_cell, "mxGeometry", relative="1", **{"as": "geometry"})

        # Генерация ID для метки связи

        label_id = f"{conn_id}_label"
        style_dict = parse_style_to_dict(_style)

        _color = style_dict['strokeColor']

        label_cell = ET.SubElement(root, "mxCell", id=label_id, value=conn[2],
                                   style=f'''whiteSpace=wrap;fontSize=9;fontColor={_color};labelBackgroundColor=#ffffff77;fontStyle=2''',
                                   vertex="1",
                                   connectable="0", parent=conn_id)

        geometry = ET.SubElement(label_cell, "mxGeometry", x="0", y="2", relative="1", **{"as": "geometry"})
        ET.SubElement(geometry, "mxPoint", **{"as": "offset"})


def generate_bpmn_drawio(diagram_name, drawio):
    """Генерация всей диаграммы в формате Draw.io (BPMN)."""

    bpmn_lanes, connections, BPMN_WIDTH =  drawio['bpmn_lanes'], drawio['connections'], drawio['BPMN_WIDTH']

    mxfile = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(mxfile, "diagram", name="Diagram 1", id="diagram1")
    mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1000", dy="1000", grid="1", gridSize="10", guides="1",
                                 tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1",
                                 pageWidth="827", pageHeight="1169", math="0", shadow="0")

    root = ET.SubElement(mxGraphModel, "root")

    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    # Генерация заголовка в пул
    header_cell = ET.SubElement(root, "mxCell", id="header", value=diagram_name,
                                style="swimlane;html=1;startSize=20;horizontal=1;", vertex="1", connectable="0",
                                parent="1")
    header_geometry = ET.SubElement(header_cell, "mxGeometry", x="0", y="30", width=BPMN_WIDTH, height="20",
                                    relative="1", **{"as": "geometry"})

    # Генерация лэйнов
    for lane_key, lane_value in bpmn_lanes.items():
        generate_lane(root, lane_key, lane_value)

    # Генерация связей
    generate_connections(root, connections)

    return ET.tostring(mxfile, encoding="unicode", method="xml")

# _def = diagrams.AGK_2025.d_10_01_supplier_operation

import argparse
import importlib
import os
import sys


def main(diagram_path):
    # Преобразуем путь к файлу в путь к модулю
    module_name = diagram_path.replace('/', '.').replace('\\', '.').rstrip('.py')
    
    try:
        # Динамически импортируем модуль
        diagram = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Модуль '{module_name}' не найден. Проверьте правильность пути.")
        sys.exit(1)
    except Exception as e:
        print(f"** Ошибка при импорте модуля '{module_name}': {e}")
        sys.exit(1)

    # Проверяем наличие необходимых атрибутов в модуле
    required_attributes = ['DIAGRAM_NAME', 'drawio']
    for attr in required_attributes:
        if not hasattr(diagram, attr):
            print(f"Модуль '{module_name}' не содержит обязательного атрибута '{attr}'.")
            sys.exit(1)

    drawio = diagram.drawio

    BPMN_WIDTH = drawio['BPMN_WIDTH']
    
    diagram_header = diagram.DIAGRAM_NAME
   
    file_out = '\\'.join(module_name.split('.')[:-1] + [f"d_{diagram_header}.drawio"])
    
    xml_output = generate_bpmn_drawio(diagram_header, drawio)

    os.makedirs(os.path.dirname(file_out), exist_ok=True)
    with open(file_out, "w", encoding="utf-8") as file:
        file.write(xml_output)

    print(f"\n\nDraw.io файл создан: [{file_out}]")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Генерация диаграммы из указанного модуля.")
    parser.add_argument("diagram_path", type=str, help="Путь к файлу диаграммы (например, diagrams/AGK_2025/d_10_01_supplier_operation.py)")
    args = parser.parse_args()
    main(args.diagram_path)
