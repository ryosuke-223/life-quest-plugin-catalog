# 日本の庭園・景勝地プラグイン実装計画

**Goal:** Life Questの公式カタログに、独立して追加できる「有名庭園」と「有名景勝地」の2つのJSONプラグインを追加する。

**Architecture:** 既存のschemaVersion 1データパックを使い、写真位置判定は単一点の円と複数地点の円で表現する。庭園プラグインは国指定の特別名勝庭園を中心に公開性と位置判定可能性で厳選し、景勝地プラグインは庭園8件を含めた自然・文化景観を、狭い名所と広域景観の混合として収録する。広域項目は公式境界の断定を避け、複数の代表地点と大きめの半径で「訪問の目安」として扱う。

**Tech Stack:** JSON manifest、Python catalog validator、Python catalog builder、Markdown data-source notes。

## Global Constraints

- プラグインからSwift、JavaScript、外部クエリを実行しない。
- `photoLocation` のみを使い、写真の撮影位置と登録地点の円形範囲を照合する。
- 広域の円は公式区域そのものではなく代表地点を含む訪問判定の目安として説明する。
- `visualizations` は固定タイプのみを使い、同一タイプを1プラグイン内で重複指定しない。
- 既存の未コミット変更を戻さず、今回のファイルだけを追加・更新する。
- `python3 scripts/validate_catalog.py`、`python3 -m unittest scripts.test_validate_catalog`、`git diff --check` を実行する。

## Task 1: 庭園プラグインのマニフェスト

**Files:**
- Create: `plugins/japan-famous-gardens.json`

- [x] 20件前後の代表庭園を地域グループ付きで登録する。
- [x] 庭園ごとに代表座標、判定半径、`photoLocation` 自動判定を指定する。
- [x] 日本三名園、東京の都立名勝庭園、京都の代表的な文化財庭園、栗林公園、毛越寺、仙巌園などを含める。
- [x] `progressSummary`、`metricCards`、`statusMap`、`groupProgress`、`lineChart`、`pieChart`、`achievementCards`、`nextAchievements`、`itemList` を指定する。
- [x] 実績は最初の1件、5件、三名園、半数、全件を表現する。
- [x] 葉を抽象化した静的SVGと、既存仕様のステータス色を指定する。

## Task 2: 景勝地プラグインのマニフェスト

**Files:**
- Create: `plugins/japan-famous-scenic-spots.json`

- [x] 庭園8件を含め、海・島、山・高原、湖・湿原、渓谷・滝、森林、火山・地形のグループを構成する。
- [x] 日本三景、国立公園の代表景観、世界自然遺産・特別名勝に関係する広域景観を登録する。
- [x] 広域項目は複数の代表地点と1,000〜5,000m程度の半径を使い、地点名だけの狭い判定にしない。
- [x] `statusMap` はクラスタリングを有効にし、`pieChart` はグループ別にする。
- [x] 実績は最初の1件、5件、庭園三名園、12件、半数、全件を表現する。
- [x] 山・波・地形を抽象化した静的SVGと、既存仕様のステータス色を指定する。

## Task 3: 出典と判定範囲の説明

**Files:**
- Create: `GARDEN_PLUGIN_DATA_SOURCES.md`
- Create: `SCENIC_SPOTS_PLUGIN_DATA_SOURCES.md`

- [x] 文化庁の名勝・特別名勝の定義と、環境省の国立公園の説明を一次資料として記録する。
- [x] 庭園の選定基準、景勝地の選定基準、庭園プラグインと景勝地プラグインの重複方針を記録する。
- [x] 代表座標が公式案内またはWikidataのCC0座標に基づくことを記録する。
- [x] 半径が公式境界ではなく、GPS誤差と広域訪問を考慮した近似であることを記録する。
- [x] 立入制限、入山規制、公開状況は出発前に管理者の最新案内を確認するよう明記する。

## Task 4: カタログ生成と検証

**Files:**
- Modify: `catalog.json`
- Test: `scripts/test_validate_catalog.py`（既存の出荷マニフェスト検証を利用）

- [x] `python3 scripts/validate_catalog.py` を実行する。
- [x] `python3 -m unittest scripts.test_validate_catalog` を実行する。
- [x] `python3 scripts/build_catalog.py` でカタログを再生成する。
- [x] `git diff --check` を実行する。
- [x] 既存プラグインがcatalog.jsonから消えていないことと、今回の2つのIDが含まれることを確認する。
