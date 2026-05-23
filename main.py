import argparse
import csv
from pathlib import Path


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GRAY = "\033[90m"


def color(text, ansi):
    return f"{ansi}{text}{RESET}"


def parse_float(value):
    if value is None or value == "":
        return 0.0
    return float(str(value).replace("$", "").replace(",", "").strip())


def money(value):
    return f"${value:,.2f}"


def signed_money(value):
    sign = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):,.2f}"


def good_money(value):
    return color(signed_money(value), GREEN if value >= 0 else RED)


def line(char="=", width=95):
    print(color(char * width, GRAY))


def title(text):
    line("=")
    print(color(text, BOLD + CYAN))
    line("=")


def section(text):
    print()
    line("-")
    print(color(text, BOLD + MAGENTA))
    line("-")


def status_text(value, good_label, bad_label):
    return color(good_label, GREEN) if value else color(bad_label, YELLOW)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="CCU Game ships CSV export")
    args = parser.parse_args()

    path = Path(args.csv_file)

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    packages = {}

    for row in rows:
        pledge_id = str(row.get("pledgeId", "")).strip()
        package_name = row.get("packageName", "").strip() or "Unknown / Standalone"
        key = pledge_id or package_name

        if key not in packages:
            packages[key] = {
                "pledge_id": pledge_id,
                "package_name": package_name,
                "msrp": parse_float(row.get("msrp")),
                "pledge": parse_float(row.get("pledge")),
                "is_meltable": row.get("isMeltable", "").lower() == "true",
                "is_giftable": row.get("isGiftable", "").lower() == "true",
                "ships": [],
            }

        packages[key]["ships"].append({
            "name": row.get("name", "").strip(),
            "insurance": row.get("insurance", "").strip(),
            "custom_name": row.get("customName", "").strip(),
        })

    package_list = list(packages.values())

    total_msrp = sum(p["msrp"] for p in package_list)
    total_pledge = sum(p["pledge"] for p in package_list)
    total_gain = total_msrp - total_pledge

    print()
    title("STAR CITIZEN FLEET VALUE REPORT")

    print(f"Unique Pledges / Packages: {color(len(package_list), YELLOW)}")
    print(f"Contained Ship Rows:       {color(len(rows), YELLOW)}")
    print(f"Total MSRP:                {color(money(total_msrp), GREEN)}")
    print(f"Total Pledge / Melt Basis: {color(money(total_pledge), YELLOW)}")
    print(f"Value Over Melt:           {good_money(total_gain)}")

    if total_msrp:
        discount = (1 - total_pledge / total_msrp) * 100
        print(f"Effective Discount:        {color(f'{discount:.2f}% below MSRP', CYAN)}")

    title("PACKAGE BREAKDOWN")

    for package in sorted(package_list, key=lambda p: p["msrp"], reverse=True):
        gain = package["msrp"] - package["pledge"]

        meltable = status_text(package["is_meltable"], "Meltable", "Not Meltable")
        giftable = status_text(package["is_giftable"], "Giftable", "Not Giftable")

        section(f"[{package['package_name']}]")

        print(f"  Pledge ID:          {color(package['pledge_id'] or 'N/A', DIM)}")
        print(f"  Package Melt Value: {color(money(package['pledge']), YELLOW)}")
        print(f"  Package MSRP Value: {color(money(package['msrp']), GREEN)}")
        print(f"  Value Over Melt:    {good_money(gain)}")

        if package["msrp"]:
            discount = (1 - package["pledge"] / package["msrp"]) * 100
            print(f"  Discount:           {color(f'{discount:.2f}%', CYAN)}")

        print(f"  Status:             {meltable} {color('|', GRAY)} {giftable}")
        print(f"  Ships in Package:   {color(len(package['ships']), YELLOW)}")
        print(f"  Ships:")

        for ship in package["ships"]:
            custom = f" [{ship['custom_name']}]" if ship["custom_name"] else ""
            insurance = ship["insurance"] or "No Insurance Listed"

            print(
                f"    {color('-', GRAY)} "
                f"{color(ship['name'], CYAN)}{color(custom, DIM)} "
                f"{color('|', GRAY)} "
                f"{color(insurance, YELLOW)}"
            )

    title("TOP VALUE PACKAGES")

    for package in sorted(package_list, key=lambda p: p["msrp"] - p["pledge"], reverse=True)[:10]:
        gain = package["msrp"] - package["pledge"]

        print(
            f"{color(package['package_name'][:55], CYAN):<70} "
            f"{good_money(gain):>20}"
        )


if __name__ == "__main__":
    main()