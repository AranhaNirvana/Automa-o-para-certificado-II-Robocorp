from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
import os

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """


    os.makedirs("robots/pdfs", exist_ok=True)
    os.makedirs("robots/robots_pngs", exist_ok=True)


    browser.configure(
        slowmo=100,
    )
    open_robot_order_website()
    download_excel_file()
    close_annoying_modal()
    get_orders()
    archive_receipts()


def open_robot_order_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")


def download_excel_file():
    """Downloads excel file from the given URL"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)


def get_orders():
    """Read data from excel and fill in the sales form"""
    tables = Tables()
    orders = tables.read_table_from_csv("orders.csv", header=True)

    for row in orders:
        fill_and_submit_orders_form(row)



def fill_and_submit_orders_form(order):
    page = browser.page()

    page.select_option("#head", str(order["Head"]))

    page.click(
        f'//*[@id="root"]/div/div[1]/div/div[1]/form/div[2]/div/div[{order["Body"]}]/label'
    )

    page.fill(
        "input[placeholder='Enter the part number for the legs']",
        str(order["Legs"])
    )

    page.fill("#address", str(order["Address"]))

    collect_results(order)

    for _ in range(5):
        page.click("#order")

        try:
            page.locator("#receipt").wait_for(
                state="visible",
                timeout=3000
            )
            break
        except:
            pass

    export_receipt_as_pdf(order)

    page.click("#order-another")

    close_annoying_modal()
    

  
def collect_results(order):
    """Take a screenshot of the page"""
    page = browser.page()

    page.click("text=Preview")

    page.screenshot(
    path=f"robots/robots_pngs/robot_{order['Order number']}.png",
)


def export_receipt_as_pdf(order):
    """Export the receipt to a pdf file"""
    page = browser.page()
    robot_receipt_html = page.locator("#receipt").inner_html()

    pdf = PDF() 
    pdf.html_to_pdf(
    robot_receipt_html,
    f"robots/pdfs/robot_{order['Order number']}.pdf"
)


def close_annoying_modal():
    page = browser.page()
    if page.locator("button:text('OK')").is_visible():
        page.click("button:text('OK')")


def archive_receipts():
    """Creates a ZIP archive of the receipts"""
    archive = Archive()
    archive.archive_folder_with_zip(
        "robots/pdfs",
        "robots/receipts.zip"
    )


