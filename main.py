from rich.table import Table
from rich.console import Console

def oblicz_rate(rrso, kwota_pozyczki, okres_splaty_mies):
    miesieczne_oprocentowanie = rrso / 12 / 100
    if miesieczne_oprocentowanie == 0:
        return kwota_pozyczki / okres_splaty_mies
    rata = kwota_pozyczki * (
        miesieczne_oprocentowanie * (1 + miesieczne_oprocentowanie) ** okres_splaty_mies
    ) / ((1 + miesieczne_oprocentowanie) ** okres_splaty_mies - 1)
    return rata

def kalkulator(rrso, wklad_wlasny, kwota_inwestycji, okres_splaty_lat):
    okres_miesiecy = okres_splaty_lat * 12
    kwota_pozyczki = kwota_inwestycji - wklad_wlasny
    rata = oblicz_rate(rrso, kwota_pozyczki, okres_miesiecy)
    calkowita_kwota = rata * okres_miesiecy
    koszt_kredytu = calkowita_kwota - kwota_pozyczki

    print(f"\n✅ Wyniki dla Twojego kredytu:")
    print(f"  ➤ Kwota inwestycji: {kwota_inwestycji:,.2f} PLN")
    print(f"  ➤ Wkład własny: {wklad_wlasny:,.2f} PLN")
    print(f"  ➤ Kwota pożyczki: {kwota_pozyczki:,.2f} PLN")
    print(f"  ➤ Okres spłaty: {okres_splaty_lat} lat")
    print(f"  ➤ Miesięczna rata: {rata:,.2f} PLN")
    print(f"  ➤ Całkowita kwota do oddania: {calkowita_kwota:,.2f} PLN")
    print(f"  ➤ Koszt kredytu: {koszt_kredytu:,.2f} PLN")

    return kwota_pozyczki

def drukuj_tabele_rich(kwota_pozyczki, dane):
    console = Console()
    table = Table(title=f"📋 Tabela dla kwoty pożyczki: {round(kwota_pozyczki):,} PLN")

    table.add_column("Okres (lata)", justify="center", style="cyan")
    table.add_column("Rata miesięczna", justify="right", style="green")
    table.add_column("Całkowita do spłaty", justify="right", style="yellow")
    table.add_column("Koszt kredytu", justify="right", style="red")

    for wiersz in dane:
        table.add_row(*wiersz)

    console.print(table)

def generuj_tabele(rrso, kwota_inwestycji, kwota_poczatkowa, okresy_lat):
    udzialy = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.70, 0.80]
    kwoty_pozyczek = [kwota_poczatkowa] + [kwota_inwestycji * u for u in udzialy]

    for kwota_pozyczki in kwoty_pozyczek:
        tabela = []
        for lata in okresy_lat:
            miesiecy = lata * 12
            rata = oblicz_rate(rrso, kwota_pozyczki, miesiecy)
            calkowita_kwota = rata * miesiecy
            koszt_kredytu = calkowita_kwota - kwota_pozyczki
            tabela.append([
                str(lata),
                f"{rata:,.2f} PLN",
                f"{calkowita_kwota:,.2f} PLN",
                f"{koszt_kredytu:,.2f} PLN"
            ])

        drukuj_tabele_rich(kwota_pozyczki, tabela)

def main():
    print("=== Kalkulator Kredytowy ===")
    try:
        rrso = float(input("Podaj RRSO (%): ").replace(',', '.'))
        kwota_inwestycji = float(input("Podaj kwotę inwestycji (PLN): ").replace(',', '.'))
        wklad_wlasny = float(input("Podaj wkład własny (PLN): ").replace(',', '.'))
        okres_splaty_lat = int(input("Podaj okres spłaty (w latach): "))
    except ValueError:
        print("⚠️ Błąd: upewnij się, że wszystkie dane są liczbami.")
        return

    kwota_pozyczki = kalkulator(rrso, wklad_wlasny, kwota_inwestycji, okres_splaty_lat)
    generuj_tabele(
        rrso,
        kwota_inwestycji,
        kwota_pozyczki,
        okresy_lat=[2, 3, 5, 8, 10, 15, 20, 25, 30]
    )

if __name__ == "__main__":
    main()
