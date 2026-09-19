# Life Quest Plugin Catalog

Life Questの公式プラグインカタログです。プラグインはSwiftコードではなく、Life Quest本体の固定判定エンジンが解釈するJSONデータとして登録します。

## ディレクトリ

```text
.
├── catalog.json              # アプリが取得する公開カタログ
├── plugins/                  # 個別プラグインの原本
├── AIRPORT_DATA_SOURCES.md   # 空港プラグインの対象範囲と出典
├── CASTLE_PLUGIN_DATA_SOURCES.md # 城郭プラグインの出典と判定範囲
├── GARDEN_PLUGIN_DATA_SOURCES.md # 庭園プラグインの選定と出典
├── SCENIC_SPOTS_PLUGIN_DATA_SOURCES.md # 景勝地プラグインの選定と判定範囲
├── scripts/
│   ├── build_catalog.py      # plugins/*.jsonからcatalog.jsonを生成
│   └── validate_catalog.py   # PR用の形式検証
└── .github/workflows/        # PR検証とGitHub Pages公開
```

## プラグイン追加の流れ

1. `plugins/` に新しいJSONを追加する。
2. `python3 scripts/validate_catalog.py` を実行する。
3. `python3 scripts/build_catalog.py` で `catalog.json` を更新する。
4. [CONTRIBUTING.md](CONTRIBUTING.md)に従い、対象データの出典、ライセンス、更新日をPR本文に記載する。
5. PRを作成し、検証ワークフローが成功した状態でレビューを受ける。
6. `main` にマージするとGitHub Pagesへ公開される。

実データを含むプラグインでは、施設名・位置情報・営業状態などの出典と、再配布可能なライセンスを必ず確認してください。仮データや出典不明のスクレイピングデータは登録しません。

## GitHub Pages設定

リポジトリの Settings → Pages → Build and deployment で、Source を **GitHub Actions** に設定します。

公開後のカタログURLは次の形式です。

```text
https://OWNER.github.io/REPOSITORY/catalog.json
```

このリポジトリの公開URLは
`https://ryosuke-223.github.io/life-quest-plugin-catalog/catalog.json` です。

Life QuestアプリのDebug／Releaseビルドで、Build Settingsの `PLUGIN_CATALOG_URL` にこのURLを設定すると、ユーザーはURLを入力せず、アプリ内の一覧からインストールできます。

## 自動判定の範囲

- `photoLocation`: 写真の撮影位置と項目の座標を固定アダプタで照合
- `healthKitAnnualStepCount`: 現在年のHealthKit歩数を固定アダプタで照合

`photoLocation` は項目の `latitude` / `longitude` で単一の円形地点を指定できます。離れた構成資産を持つ項目には、`locations` 配列で複数の地点を指定します。各地点は従来の座標・半径のほか、GeoJSONの `Polygon` / `MultiPolygon` を判定範囲にできます。円形地点は座標から半径内、ポリゴン地点は外周の内側かつ穴の外側に撮影座標が入ると、その親項目を1件だけ訪問候補にします。地点数が増えても項目数や実績の達成数は増えません。旧形式の単一座標と円形地点も引き続き有効です。

各地点には一意な `id` と表示用 `title` を指定します。円形地点では `latitude`、`longitude`、任意の `radiusMeters` を使います。範囲地点では `geometry` に `Polygon` または `MultiPolygon` を指定し、座標はGeoJSONに従って `[longitude, latitude]` の順にします。リングは4点以上で始点と終点を一致させ、最初のリングを外周、後続リングを除外する穴として記述します。外周上は範囲内、穴の境界と内側は範囲外として扱います。MultiPolygonは離れた複数のポリゴンを表します。範囲地点で表示用ピンも必要な場合は、`latitude` と `longitude` を両方指定できますが、`radiusMeters` とは併用できません。ポリゴン座標の総数はプラグインあたり50,000点までです。座標と構成資産名の出典はプラグインの説明資料またはPRに記録してください。複数地点を使う場合は、旧形式の項目直下の座標と混在させません。地図の帰属表示には任意のトップレベル文字列 `mapAttribution` を使い、指定した文字列を地図の下に表示します。

```json
{
  "id": "historic-example",
  "title": "複数の構成資産を持つ遺産",
  "automation": { "type": "photoLocation" },
  "locations": [
    {
      "id": "component-a",
      "title": "構成資産A",
      "latitude": 35.0,
      "longitude": 139.0,
      "radiusMeters": 200
    },
    {
      "id": "castle-grounds",
      "title": "城郭内",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [139.0, 35.0], [139.01, 35.0], [139.01, 35.01],
          [139.0, 35.01], [139.0, 35.0]
        ]]
      }
    }
  ]
}
```

地点の出典URLはマニフェストに含めません。座標・構成資産名などの根拠は、プラグインの説明資料（`*_DATA_SOURCES.md` など）とPR本文に記録します。OSM由来の座標を使う場合は [OpenStreetMapへの帰属表示とODbL](https://www.openstreetmap.org/copyright) に従い、プラグインとソースデータ説明にライセンスを明記してください。

### 地図マーカーの表示設定

地図の形状と色は、プラグインの任意の `mapStyle` で指定します。`markerSVG` は `svg`、`g`、`path` だけを使った静的なシルエットで、実行コード・外部参照・画像・CSS・変形・フィルターは使えません。`viewBox` を必須とし、パス命令は `M/m`、`L/l`、`H/h`、`V/v`、`C/c`、`Q/q`、`Z/z` に限ります。SVGは20,000バイト以下です。

`markerColors` はマーカー、`areaFillColors` は円・ポリゴンの塗り、`areaStrokeColors` は円・ポリゴンの線に使われます。各オブジェクトには `unvisited`、`estimated`、`confirmed` を必ず指定し、色は `#RRGGBB` または `#RRGGBBAA` で記述します。`mapStyle` を省略した場合は標準の無地ピンとアプリの互換デフォルト色を使います。

```json
"mapStyle": {
  "markerSVG": "<svg viewBox=\"0 0 36 36\"><path d=\"M3 32V24h30v8H3z\"/></svg>",
  "markerColors": {
    "unvisited": "#8E8E93",
    "estimated": "#007AFF",
    "confirmed": "#FF9500"
  },
  "areaFillColors": {
    "unvisited": "#D1D1D638",
    "estimated": "#007AFF59",
    "confirmed": "#FF950073"
  },
  "areaStrokeColors": {
    "unvisited": "#8E8E93",
    "estimated": "#007AFF",
    "confirmed": "#FF9500"
  }
},
"groups": [
  { "id": "cultural", "title": "文化遺産", "mapMarkerSVG": "<svg viewBox=\"0 0 36 36\"><path d=\"M3 30h30v3H3z\"/></svg>" }
]
```

グループの `mapMarkerSVG` は、そのグループに属する項目だけ形状を上書きします。グループSVG、プラグインSVG、既存の `mapMarkerSymbolName`、標準の無地ピンの順にフォールバックします。`mapMarkerSymbolName` は既存プラグインとの互換用で、新しいプラグインでは `mapStyle` を使ってください。

### 日本の世界遺産めぐり

[世界遺産プラグイン](plugins/japan-world-heritage.json)には、日本の世界遺産27件を親項目として登録し、文化・自然遺産あわせて251地点を設定しています。写真の位置が同じ遺産に設定した地点のどれか1つから200m以内なら、その親項目を1件達成します。自然遺産の島全体を覆う大きな円は使わず、登録区域内の登山・散策などの代表地点で判定します。参詣道などの線状資産も公式案内上の代表地点による判定で、登録区域全体を境界判定するものではありません。宗像の沖ノ島本島は立入不可のため項目説明に表示し、GPS判定と達成カウントの対象外とします。座標の根拠、除外理由、通行・立入上の注意は[座標判定の調査メモ](WORLD_HERITAGE_COORDINATE_RESEARCH.md)と[データ出典](WORLD_HERITAGE_DATA_SOURCES.md)を参照してください。

## 可視化の指定

プラグインは任意のSwiftUIコードを配布できません。`visualizations` には、アプリに組み込まれた固定可視化のタイプと、対象データ・集計方法だけを指定します。これはKibanaのパネル定義に近い方式です。

### 共通ルール

- `visualizations` は省略可能です。省略時はアプリの後方互換デフォルトを使います。
- 同じ `type` は1プラグイン内で1回だけ指定します。
- 可視化の宣言順が詳細画面での表示順になります。
- `showsPeriodSelector` は任意の真偽値です。省略時は `true`（期間選択を表示）として扱います。期間選択を使わないプラグインだけ `false` を指定できます。
- `annualCount` と `cumulativeCount` は項目の `firstVisitYear` を使った初訪問集計です。
- `annualVisitedItemCount` は項目ごとの訪問年履歴を使い、同じ「項目ID × 暦年」を1回として、その年に訪問記録がある項目数を集計します。
- 期間の「すべて」は現在の全状態、「2025年まで」は2025年末時点の累積状態です。
- 年次チャートの `annualCount` は、その年に初訪問した項目数です。
- `cumulativeCount` は、その年までに初訪問した項目数です。
- 年の途中に記録がない年も年軸から省かず、年別値は0、累積値は直前年の値を維持します。記録のない末尾年や現在年は追加しません。
- `completionRate` は、累積訪問項目数 ÷ 全項目数です。
- グループ進捗は初期状態で折りたたみ、展開したときだけ所属項目を表示します。
- `itemList` は詳細画面に全件を並べず、件数と「一覧を見る」導線から専用一覧画面を開きます。長い共通説明は一覧項目ごとに繰り返さず、必要な場合は一覧画面の `?` ヘルプにまとめます。
- `item.detail` は所在地など項目固有の補足に使います。写真位置による自動判定や判定半径は `automation` と `radiusMeters` から共通ヘルプで説明するため、項目詳細に重複して記述しません。

### 対応タイプとパラメータ

| type | 必須・任意パラメータ | 用途 |
| --- | --- | --- |
| `progressSummary` | なし | プラグイン名、説明、全体進捗 |
| `metricCards` | `metrics` | 複数のサマリーメトリクス |
| `lineChart` | `metric`、`aggregation` | 年次推移の線グラフ |
| `barChart` | `metric`、`aggregation` | 年次比較の棒グラフ |
| `areaChart` | `metric`、`aggregation` | 累積・推移の面グラフ |
| `pieChart` | `breakdown` | 状態またはグループの割合 |
| `heatmap` | `dimension` | 年×グループ／年×状態 |
| `achievementCards` | なし | 実績の解除状況 |
| `groupProgress` | なし | `groups` ごとの進捗。グループ必須 |
| `statusMap` | `cluster` | 座標項目の地図。座標項目必須 |
| `statusGrid` | `columns` | 項目状態のグリッド。2〜6列 |
| `nextAchievements` | `limit` | 未解除実績。1〜10件 |
| `itemList` | `sort` | 項目一覧。状態・タイトル・グループ順 |

### 指定できる値

`metricCards.metrics` とチャートの `metric` は次から選びます。

| metric | 意味 |
| --- | --- |
| `visitedCount` | 期間内に訪問済みの項目数 |
| `completionRate` | 期間内の達成率。0〜1を画面でパーセント表示 |
| `remainingCount` | 全項目数から訪問済み項目数を引いた数 |
| `unlockedAchievements` | 期間時点で解除済みの実績数 |
| `totalAchievements` | プラグインに定義された実績数 |

`aggregation` は次の4種類です。

| aggregation | 意味 |
| --- | --- |
| `annualCount` | `firstVisitYear` がその年の項目数。初訪問の年次棒グラフ向け |
| `annualVisitedItemCount` | その年に訪問履歴がある項目数。同一項目・同一暦年は1回。訪問年別の棒グラフ向け |
| `cumulativeCount` | その年以下の `firstVisitYear` を持つ項目数。累積線・エリアグラフ向け |
| `completionRate` | 累積訪問項目数を全項目数で割った値 |

`pieChart.breakdown` は `status`（未訪問・推定・確認済み）または `group`（グループ別）です。`heatmap.dimension` は `yearByGroup`（年×グループの初訪問数）または `yearByStatus`（年までの状態別項目数）です。

### JSON例

```json
"visualizations": [
  {
    "type": "metricCards",
    "metrics": ["visitedCount", "completionRate", "remainingCount"]
  },
  {
    "type": "lineChart",
    "metric": "visitedCount",
    "aggregation": "cumulativeCount"
  },
  {
    "type": "barChart",
    "metric": "visitedCount",
    "aggregation": "annualVisitedItemCount"
  },
  { "type": "groupProgress" },
  { "type": "itemList", "sort": "group" }
],
"showsPeriodSelector": false
```

不明なタイプ・値、重複タイプ、範囲外の列数や件数は、アプリと `scripts/validate_catalog.py` の両方で拒否されます。実行コード、任意のクエリ、任意のSwiftUIを受け付けません。

プラグインから任意のSwiftコード、JavaScript、外部クエリを実行することはできません。
