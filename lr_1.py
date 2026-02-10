import requests
import matplotlib.pyplot as plt
import pandas as pd


def get_stat(stats_list, stat_name: str) -> int:
    """Достаёт значение статы (hp/attack/defense и т.д.) из списка stats."""
    for item in stats_list:
        if item["stat"]["name"] == stat_name:
            return int(item["base_stat"])
    return 0


def main():
    base_url = "https://pokeapi.co/api/v2/"
    limit = 10
    url = f"{base_url}pokemon?limit={limit}"

    # 1) Получаем список покемонов
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    listing = resp.json()["results"]

    # 2) Парсим каждого покемона по ссылке и собираем нужные поля
    data = []
    for p in listing:
        p_resp = requests.get(p["url"], timeout=20)
        p_resp.raise_for_status()
        p_json = p_resp.json()

        item = {
            "id": p_json["id"],
            "name": p_json["name"],
            "height": p_json["height"],
            "weight": p_json["weight"],
            "hp": get_stat(p_json["stats"], "hp"),
            "attack": get_stat(p_json["stats"], "attack"),
            "defense": get_stat(p_json["stats"], "defense"),
            "speed": get_stat(p_json["stats"], "speed"),
            "base_experience": p_json.get("base_experience", 0),
            "types": ", ".join(t["type"]["name"] for t in p_json["types"]),
        }
        data.append(item)

    df = pd.DataFrame(data).sort_values("id")
    print(df[["id", "name", "height", "weight", "hp", "attack", "defense", "speed", "base_experience", "types"]])

    names = df["name"].tolist()

    # -------------------- 1) Линейный график --------------------
    plt.figure()
    plt.plot(names, df["hp"].tolist(), marker="o")
    plt.title("HP (здоровье) у покемонов")
    plt.xlabel("Покемон")
    plt.ylabel("HP")
    plt.xticks(rotation=45, ha="right")

    for x, y in zip(names, df["hp"].tolist()):
        plt.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 6))
    plt.tight_layout()

    # -------------------- 2) Точечная диаграмма --------------------
    plt.figure()
    plt.scatter(df["attack"], df["defense"])
    plt.title("Attack vs Defense")
    plt.xlabel("Attack")
    plt.ylabel("Defense")

    for _, row in df.iterrows():
        plt.annotate(row["name"], (row["attack"], row["defense"]), textcoords="offset points", xytext=(0, 6))
    plt.tight_layout()

    # -------------------- 3) Столбчатая диаграмма --------------------
    plt.figure()
    plt.bar(names, df["weight"].tolist())
    plt.title("Вес покемонов")
    plt.xlabel("Покемон")
    plt.ylabel("Weight")
    plt.xticks(rotation=45, ha="right")
    for x, y in zip(names, df["weight"].tolist()):
        plt.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 6))
    plt.tight_layout()

    # -------------------- 4) Горизонтальная столбчатая --------------------
    plt.figure()
    plt.barh(names, df["height"].tolist())
    plt.title("Рост (height) покемонов")
    plt.xlabel("Height")
    plt.ylabel("Покемон")

    for y_name, val in zip(names, df["height"].tolist()):
        plt.annotate(str(val), (val, y_name), textcoords="offset points", xytext=(0, 6))
    plt.tight_layout()

    # -------------------- 5) Гистограмма --------------------
    plt.figure()
    plt.hist(df["base_experience"].tolist(), bins=6)
    plt.title("Распределение base_experience")
    plt.xlabel("base_experience")
    plt.ylabel("Количество покемонов")
    plt.tight_layout()

    # -------------------- 6) Круговая диаграмма --------------------
    plt.figure()
    values = df["attack"].tolist()
    plt.pie(values, labels=names, autopct="%1.1f%%")
    plt.title("Доли Attack среди выбранных покемонов")
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
