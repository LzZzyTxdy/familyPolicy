import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import CRUD


def get_desktop_path():
    """
    获取当前用户的桌面路径
    :return: 桌面路径
    """
    return os.path.join(os.path.expanduser('~'), 'Desktop')


def save_one_warranty_to_pdf(name: str, warrantyNum: str) -> None:
    """
    输出某人某张保单的pdf
    :param name: 姓名
    :param warrantyNum: 保单号
    :return: None
    """

    data = CRUD.get_one_warranty(warrantyNum)
    desktop_path = get_desktop_path()
    file_path = os.path.join(desktop_path, f"{name}'s warranty ({warrantyNum}).pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'title',
        parent=styles['Title'],
        fontSize=14  # 调整标题字体大小
    )

    title = Paragraph(f"{name}\'s warranty({warrantyNum})", title_style)
    elements.append(title)

    data1 = data.loc[:, 'name':'birthday']
    data2 = data.loc[:, 'company':'warranty_number']
    data3 = data.loc[:, 'premium':'effective_date']
    data4 = data.loc[:, 'product_type':'duration']

    # 格式化表格数据
    # 根据需要调整这些宽度，总和应不超过540点
    data_list1 = [data1.columns.tolist()] + data1.values.tolist()
    data_list1 = [[str(cell) for cell in row] for row in data_list1]  # 确保所有单元格数据转换为字符串
    col_widths1 = [180, 180, 180]
    table1 = Table(data_list1, colWidths=col_widths1)

    data_list2 = [data2.columns.tolist()] + data2.values.tolist()
    data_list2 = [[str(cell) for cell in row] for row in data_list2]  # 确保所有单元格数据转换为字符串
    col_widths2 = [135, 270, 135]
    table2 = Table(data_list2, colWidths=col_widths2)

    data_list3 = [data3.columns.tolist()] + data3.values.tolist()
    data_list3 = [[str(cell) for cell in row] for row in data_list3]  # 确保所有单元格数据转换为字符串
    col_widths3 = [135, 135, 135, 135]
    table3 = Table(data_list3, colWidths=col_widths3)

    data_list4 = [data4.columns.tolist()] + data4.values.tolist()
    data_list4 = [[str(cell) for cell in row] for row in data_list4]  # 确保所有单元格数据转换为字符串
    col_widths4 = [180, 180, 180]
    table4 = Table(data_list4, colWidths=col_widths4)

    # data_list = [data.columns.tolist()] + data.values.tolist()
    # data_list = [[str(cell) for cell in row] for row in data_list]  # 确保所有单元格数据转换为字符串

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # 使用标准字体
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 调整字体大小
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),  # 增加单元格的左右边距
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ])

    table1.setStyle(style)
    table2.setStyle(style)
    table3.setStyle(style)
    table4.setStyle(style)

    elements.append(table1)
    elements.append(table2)
    elements.append(table3)
    elements.append(table4)

    doc.build(elements)
    print(f'已将{name}的{warrantyNum}号保单全部保单信息输出至pdf文档中')


def save_all_warranties_to_pdf(name: str) -> None:
    """
    输出某人全部保单的pdf文档
    :param name: 姓名
    :return: None
    """
    desktop_path = get_desktop_path()
    file_path = os.path.join(desktop_path, f"{name}'s warranties.pdf")

    # 调用一个函数获取指定人的保单数据
    data = CRUD.get_all_warranties(f'{name}')

    # 创建一个PDF文档模板，指定页面大小为letter（美国信纸大小）
    doc = SimpleDocTemplate(file_path, pagesize=letter)

    # 初始化一个空列表，用于存储将要添加到文档中的元素
    elements = []

    # 调用一个函数获取样式表，这个函数的定义不在这段代码中
    styles = getSampleStyleSheet()

    # 创建一个标题样式，继承自样式表中的'Title'样式，并设置字体大小为14
    title_style = ParagraphStyle(
        'title',
        parent=styles['Title'],
        fontSize=14  # 调整标题字体大小
    )

    # 创建标题段落，并使用上面定义的标题样式
    title = Paragraph(f"{name}'s warranties", title_style)
    # 将标题添加到元素列表中
    elements.append(title)

    # 格式化表格数据，确保DataFrame的列名和数据都转换为字符串
    data_list = [data.columns.tolist()] + data.values.tolist()
    data_list = [[str(cell) for cell in row] for row in data_list]

    # 设置表格的列宽，总宽度为540点，根据需要调整各列宽度
    col_widths = [90, 40, 40, 80, 180, 35, 45, 30]

    # 创建一个表格对象，传入数据和列宽
    table = Table(data_list, colWidths=col_widths)

    # 设置表格样式，包括背景色、文本颜色、对齐方式、字体、字体大小、边距、网格线等
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ])
    # 应用设置的样式到表格
    table.setStyle(style)

    # 将表格添加到元素列表中
    elements.append(table)

    # 使用文档模板构建PDF文档，元素列表中的元素将被添加到文档中
    doc.build(elements)

    # 打印信息到控制台，告知用户PDF文档已生成
    print(f'已将{name}的全部保单信息输出至pdf文档中')


# 读取PDF文件
def read_pdf_binary(file_path):
    with open(file_path, "rb") as file:
        pdf_binary_data = file.read()
    # print(pdf_binary_data)
    return pdf_binary_data


def is_pdf_file_by_content(file_path):
    try:
        with open(file_path, 'rb') as file:
            header = file.read(5)
            return header == b'%PDF-'
    except Exception as e:
        print(f"Error reading file: {e}")
        return False


def add_one_pdf_to_SQLServer_Path(warrantyNum, path) -> bool:
    """
    将pdf存储到SQLServer
    :param warrantyNum: 保单号
    :param path: 文件路径
    :return: True:添加成功；False:添加失败
    """
    cursor, connect = CRUD.connectToSQL()
    try:
        pdf_text = read_pdf_binary(path)
        # print(pdf_text)

        # 插入PDF数据到数据库
        cursor.execute(f"INSERT INTO pdf_ VALUES ({warrantyNum}, %s)", (pdf_text,))
        connect.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connect.close()


def add_one_pdf_to_SQLServer_Content(warrantyNum, file_content):
    """
    将pdf存储到SQLServer
    :param warrantyNum: 保单号
    :param file_content: 文件内容
    :return: True:添加成功；False:添加失败
    """
    cursor, connect = CRUD.connectToSQL()

    try:
        cursor.execute(f"INSERT INTO pdf_ VALUES ({warrantyNum}, %s)", (file_content,))
        connect.commit()

        cursor.close()
        connect.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def read_one_pdf_from_SQLServer(warrantyNum) -> bool:
    cursor, connect = CRUD.connectToSQL()

    desktop_path = get_desktop_path()
    pdf_file_path = os.path.join(desktop_path, f"warranty ({warrantyNum}) from SQL.pdf")

    # 保存PDF文件的路径
    # pdf_file_path = f"warranty({warrantyNum}) from SQL.pdf"

    select_sql = f"SELECT pdf FROM pdf_ WHERE warranty_number = {warrantyNum}"
    cursor.execute(select_sql)
    row = cursor.fetchone()
    if row:
        pdf_text = row[0]
    else:
        # 关闭连接
        cursor.close()
        connect.close()
        return False

    if pdf_text:
        # 保存到PDF文件
        with open(pdf_file_path, 'wb') as file:
            file.write(pdf_text)
        print(f"PDF内容已成功保存到文件：{pdf_file_path}")
        # 关闭连接
        cursor.close()
        connect.close()
        return True
    else:
        print(f"没有找到保单号为{warrantyNum}的PDF内容")
        # 关闭连接
        cursor.close()
        connect.close()
        return False


