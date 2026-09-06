# 空港プラグインの対象範囲と出典

## 日本版

`japan-airports.json` は、国土交通省が分類する「拠点空港」28空港を対象にしています。地方管理空港、その他の空港、共用空港、ヘリポートは初版の対象外です。

- 対象範囲: 拠点空港28空港
- 対象範囲の出典: [国土交通省 空港一覧](https://www.mlit.go.jp/koku/15_bf_000310.html)
- 座標の出典: [OurAirports airports.csv](https://github.com/davidmegginson/ourairports-data)
- 座標データのライセンス: OurAirportsの公開情報ではPublic Domain

## 海外版

`world-major-airports.json` は、OurAirportsのデータからIATAコードを持つ主要国際空港を地域別にキュレーションした100空港です。世界中の全空港や、旅客数順の公式ランキングではありません。小規模空港や同一都市の二つ目以降の空港をすべて含めず、利用者が進捗を把握しやすい規模にしています。

- 対象範囲: 主要国際空港100空港
- 地域: 東アジア、東南アジア、南アジア、中東、ヨーロッパ、北米、中南米、オセアニア、アフリカ
- データの出典: [OurAirports open data](https://ourairports.com/data/)
- 座標データのライセンス: OurAirportsの公開情報ではPublic Domain
- 生成基準日: 2026-09-06

## 自動判定の線引き

各項目の座標から半径1,500m以内に撮影位置付き写真がある場合、訪問を「推定」として記録します。空港の敷地は広く、公開座標が滑走路・敷地中央・ターミナルのいずれを指すかは空港ごとに異なるため、確定的な搭乗証明ではありません。利用者はアプリ内で手動修正できます。

データを更新するときは、CSVを取得して次を実行します。

```bash
curl -fsSL https://raw.githubusercontent.com/davidmegginson/ourairports-data/main/airports.csv \
  -o /tmp/ourairports-airports.csv
python3 scripts/generate_airport_plugins.py /tmp/ourairports-airports.csv
python3 scripts/validate_catalog.py
python3 scripts/build_catalog.py
```
