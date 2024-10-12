import time

import flet as ft

import stamp_solver


def print_result(results: list[stamp_solver.StampSet]) -> tuple[str, str]:
    residual = ""
    text = ""
    if len(results) > 0:
        residual = f"residual: {results[0].residual}"
        for result in results:
            text += str(result.stamps)
            text += "\n"
    else:
        residual = None
        text = None
    return residual, text


def main(page: ft.Page):
    def button_clicked(e):
        residual_txt.value = "SOLVING..."
        result_text.value = "SOLVING..."
        residual_txt.color = "orange"
        result_text.color = "orange"
        page.update()
        residual = None
        result = None
        stamps = []
        for controls in controls_row:
            text_stamp, text_num = controls
            stamp_value = text_stamp.value
            stamp_num = text_num.value
            if stamp_value and stamp_num:
                try:
                    stamp_value = int(stamp_value)
                    stamp_num = int(stamp_num)
                except ValueError:
                    continue
                temp_stamps = [stamp_value for _ in range(stamp_num)]
                stamps.extend(temp_stamps)
        target_price_value = target_price_text.value
        if target_price_value:
            target_price = -1
            try:
                target_price = int(target_price_value)
            except ValueError:
                pass
        if target_price > 0:
            start = time.perf_counter()
            result = stamp_solver.solve_stamps(target_price, stamps)
            end = time.perf_counter()
            elapsed = end - start
            residual, result = print_result(result)

        if residual and result:
            residual_txt.value = residual
            result_text.value = result
            elapsed_text.value = f"elapsed time:{elapsed * 1000 * 1000} usec"
            residual_txt.color = "green"
            result_text.color = "green"
        else:
            residual_txt.value = "NoResult"
            result_text.value = "NoResult"
            residual_txt.color = "red"
            result_text.color = "red"
        page.update()

    page.title = "stamp solver"
    page.window_width = 500
    page.window_height = 800
    page.add(ft.Text("TargetPrice"))
    target_price_text = ft.TextField(label="Target Price", width=200)
    page.add(target_price_text)
    page.add(ft.ElevatedButton("solve", on_click=button_clicked))

    controls_row = []
    for i in range(5):
        controls = []
        controls.append(ft.TextField(label=f"Stamp price #{i + 1}", width=200))
        controls.append(ft.TextField(label=f"Num stamps # {i + 1}", width=200))
        page.add(ft.Row(controls=controls))
        controls_row.append(controls)
    page.add(ft.Text("Residual"))
    residual_txt = ft.Text("NoResult", color="red")
    page.add(residual_txt)
    page.add(ft.Text("Stamps"))
    result_text = ft.Text("NoResult", color="red")
    page.add(result_text)
    elapsed_text = ft.Text("---")
    page.add(elapsed_text)


ft.app(main)
