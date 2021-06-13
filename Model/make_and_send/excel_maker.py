import os
import openpyxl as excel
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
from datetime import datetime as dt

from Model.data_manager import DataManager


def adjust_column_width_from_col(ws, min_row, min_col, max_col):
    column_widths = []

    for i, col in \
            enumerate(
                ws.iter_cols(min_col=min_col, max_col=max_col, min_row=min_row)
            ):

        for cell in col:
            value = cell.value
            if value is not None:

                if isinstance(value, str) is False:
                    value = str(value)

                try:
                    column_widths[i] = max(column_widths[i], len(value))
                except IndexError:
                    column_widths.append(len(value))

    for i, width in enumerate(column_widths):
        col_name = get_column_letter(min_col + i)
        value = column_widths[i] + 20
        ws.column_dimensions[col_name].width = value


def get_right_size(wi, he):
    ratio = wi / he
    if ratio > 0:
        he, wi = 200, 200 * ratio
    else:
        wi, he = 200, 200 * ratio
    return int(wi), int(he)


def xuatFileExcel(listDuLieuTemp, tenFileXuatTemp):
    ghiData = excel.Workbook()
    trangTinh = ghiData.active
    trangTinh.title = "Sheet1"
    title_font = Font(size=27, bold=True)
    normal_font = Font(size=20)

    alignment = Alignment(horizontal="center", vertical="center")

    trangTinh.append(("   Employee ID   ","     Employee Name     ", "    Unit Of Work    ",
                      "    Arrived Time    ","    Using backup     ","          Image          "))
    a = trangTinh['A1:F1']
    for temp in a[0]:
        temp.font = title_font

    adjust_column_width_from_col(trangTinh, 1,1, trangTinh.max_column)
    inDexCell = 1

    for index, tempData in enumerate(listDuLieuTemp):
        HinhCanNhap = "test.jpg"
        imgExcel = excel.drawing.image.Image(HinhCanNhap)
        imgExcel.height, imgExcel.width = get_right_size(imgExcel.height, imgExcel.width)
        imgExcel.anchor = f'F{inDexCell+1}'
        trangTinh.merge_cells(f'F{inDexCell+1}:F{inDexCell + 10}')
        trangTinh.add_image(imgExcel)

        trangTinh.append((
            tempData[0], tempData[1], tempData[2], tempData[3], tempData[4]
        ))

        a = trangTinh[f'A{inDexCell+2}:F{inDexCell+2}']
        print(inDexCell,"this")
        inDexCell += 10

        for temp in a[0]:
            temp.font = normal_font
            temp.alignment = alignment
        if tempData[4] == 1:
            ft = Font(color="00FF0000", size=20)
            for temp in a[0]:
                temp.font = ft
                temp.alignment = alignment
    ghiData.save(filename=tenFileXuatTemp)


def read_token_and_pass():
    sheet = excel.load_workbook(filename="secret_infor.xlsx")
    data = sheet['Sheet1']
    temp_data = []
    for index, temp_value in enumerate(data.values):
        if index == 0:
            continue
        if temp_value[0] is None:
            break
        temp_data.append(temp_value)
    return temp_data


def create_excel(ID_Recorder):
    # secret_infor = read_token_and_pass()
    # print(secret_infor,"<- word later on")

    path_model = "Summary"

    # with DataManager('Model/data/database/database.db') as db:
    with DataManager('../data/database/database.db') as db:
        data_export = db.get_list_to_export(ID_RECORDER=ID_Recorder)

    # sub a space to make from "2021-06-13 02:30:22" to "2021-06-13_02h30m22"

    date_obj = dt.strptime(ID_Recorder, '%Y-%m-%d %H:%M:%S')
    format_excel_name = dt.strftime(date_obj, '%Y-%m-%d_%Ih%Mm%S')

    tenFileXuatExcel = path_model + "\\" + format_excel_name + ".xlsx"
    xuatFileExcel(data_export, tenFileXuatExcel)
    print("Done with excel work")


create_excel("2021-06-12 23:11:08")



# def openThuMuc():
#     os.startfile(f'{os.path.realpath("")}')
#
# def taoThuMucTheoThoiGian(folder_name):
#     if os.path.isfile(folder_name):
#         os.mkdir(folder_name)
#         return False
#     return True
#
# isExist = taoThuMucTheoThoiGian(ID_Recorder)
# if isExist:
#     print("Exist So do nothing")
# else:
#     print("Create")
