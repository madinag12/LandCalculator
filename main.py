import flet as ft

def main(page: ft.Page):
    page.title = "K-M-F Land Calculator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "auto"
    page.padding = 20
    page.window_width = 400  # Mobile size ki width
    page.window_height = 800

    # Data lists
    entries_data = []
    display_data = []
    edit_index = [-1] # Using list to make it mutable inside functions

    # --- UI Elements ---
    kanal_input = ft.TextField(label="Kanal", keyboard_type=ft.KeyboardType.NUMBER, expand=1, border_radius=10)
    marla_input = ft.TextField(label="Marla", keyboard_type=ft.KeyboardType.NUMBER, expand=1, border_radius=10)
    sqft_input = ft.TextField(label="Sqft", keyboard_type=ft.KeyboardType.NUMBER, expand=1, border_radius=10)
    
    conv_dropdown = ft.Dropdown(
        label="Marla Size (Sqft)",
        value="272.25",
        options=[ft.dropdown.Option("272.25"), ft.dropdown.Option("272"), ft.dropdown.Option("225")],
        border_radius=10
    )

    total_text = ft.Text("Grand Total: 0K - 0M - 0 Sqft", size=20, weight="bold", color="green")
    
    persons_input = ft.TextField(label="Persons", keyboard_type=ft.KeyboardType.NUMBER, width=100, border_radius=10)
    share_text = ft.Text("Share: 0K - 0M - 0 Sqft", size=16, weight="bold", color="blue")

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Type")),
            ft.DataColumn(ft.Text("K-M-S")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=[],
    )

    # --- logic ---
    def update_ui():
        marla_val = float(conv_dropdown.value)
        total_sqft = sum(entries_data)
        
        # Grand Total Calculation
        abs_sqft = abs(total_sqft)
        res_k = int(abs_sqft // (20 * marla_val))
        rem = abs_sqft % (20 * marla_val)
        res_m = int(rem // marla_val)
        res_s = round(rem % marla_val, 2)
        
        sign = "-" if total_sqft < 0 else ""
        total_text.value = f"Grand Total: {sign}{res_k}K - {res_m}M - {res_s} Sqft"
        
        # Refresh Table
        table.rows.clear()
        for i, (s_val, k, m, f) in enumerate(display_data):
            type_icon = "+" if s_val == 1 else "-"
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(type_icon)),
                ft.DataCell(ft.Text(f"{int(k)}K-{int(m)}M-{f}S")),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, idx=i: edit_entry(idx), icon_size=18),
                    ft.IconButton(ft.icons.DELETE, icon_color="red", on_click=lambda e, idx=i: delete_entry(idx), icon_size=18),
                ]))
            ]))
        page.update()

    def add_data(e, sign):
        try:
            k = float(kanal_input.value or 0)
            m = float(marla_input.value or 0)
            s = float(sqft_input.value or 0)
            m_val = float(conv_dropdown.value)
            
            sqft_total = sign * ((k * 20 * m_val) + (m * m_val) + s)

            if edit_index[0] != -1:
                entries_data[edit_index[0]] = sqft_total
                display_data[edit_index[0]] = (sign, k, m, s)
                edit_index[0] = -1
                btn_add.text = "ADD AREA (+)"
                btn_add.bgcolor = ft.colors.GREEN
            else:
                entries_data.append(sqft_total)
                display_data.append((sign, k, m, s))
            
            kanal_input.value = ""; marla_input.value = ""; sqft_input.value = ""
            update_ui()
        except:
            pass

    def delete_entry(idx):
        entries_data.pop(idx)
        display_data.pop(idx)
        update_ui()

    def edit_entry(idx):
        edit_index[0] = idx
        s, k, m, f = display_data[idx]
        kanal_input.value = str(k)
        marla_input.value = str(m)
        sqft_input.value = str(f)
        btn_add.text = "UPDATE"
        btn_add.bgcolor = ft.colors.ORANGE
        page.update()

    def divide(e):
        try:
            p = float(persons_input.value or 1)
            m_val = float(conv_dropdown.value)
            share = sum(entries_data) / p
            abs_s = abs(share)
            rk = int(abs_s // (20 * m_val))
            rm = int((abs_s % (20 * m_val)) // m_val)
            rs = round(abs_s % m_val, 2)
            share_text.value = f"Per Person: {rk}K - {rm}M - {rs}S"
            page.update()
        except: pass

    btn_add = ft.ElevatedButton("ADD AREA (+)", on_click=lambda e: add_data(e, 1), bgcolor=ft.colors.GREEN, color="white", expand=True)
    btn_sub = ft.ElevatedButton("SUBTRACT (-)", on_click=lambda e: add_data(e, -1), bgcolor=ft.colors.RED_ACCENT, color="white", expand=True)

    # UI Layout
    page.add(
        ft.Column([
            ft.Text("Land Area Calculator", size=24, weight="bold"),
            ft.Text("By: Muhammad Majid Khan", color="grey"),
            ft.Divider(),
            ft.Row([kanal_input, marla_input, sqft_input]),
            conv_dropdown,
            ft.Row([btn_add, btn_sub]),
            ft.Divider(),
            total_text,
            ft.Container(content=ft.Column([table], scroll=ft.ScrollMode.ALWAYS), height=200, border=ft.border.all(1, "grey")),
            ft.Divider(),
            ft.Row([persons_input, ft.ElevatedButton("Divide", on_click=divide, bgcolor=ft.colors.BLUE, color="white")]),
            share_text
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)