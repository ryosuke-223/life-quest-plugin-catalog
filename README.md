# Life Quest Plugin Catalog

Life Questの公式プラグインカタログです。プラグインはSwiftコードではなく、Life Quest本体の固定判定エンジンが解釈するJSONデータとして登録します。

## ディレクトリ

```text
.
├── catalog.json              # アプリが取得する公開カタログ
├── plugins/                  # 個別プラグインの原本
├── AIRPORT_DATA_SOURCES.md   # 空港プラグインの対象範囲と出典
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

Life QuestアプリのReleaseビルドで、Build Settingsの `PLUGIN_CATALOG_URL` にこのURLを設定すると、ユーザーはURLを入力せず、アプリ内の一覧からインストールできます。

## 自動判定の範囲

- `photoLocation`: 写真の撮影位置と項目の座標を固定アダプタで照合
- `healthKitAnnualStepCount`: 現在年のHealthKit歩数を固定アダプタで照合

## 可視化の指定

プラグインは任意のSwiftUIコードを配布できませんが、`visualizations` でアプリ内の固定ビューを選択できます。Kibanaのパネル定義に近い形式で、可視化タイプと対象データ・集計方法だけを宣言します。

- `metricCards`: `metrics` に `visitedCount`、`completionRate`、`remainingCount`、`unlockedAchievements`、`totalAchievements`
- `lineChart`、`barChart`、`areaChart`: `metric` と `aggregation`（`cumulativeCount`、`annualCount`、`completionRate`）
- `pieChart`: `breakdown`（`status`、`group`）
- `heatmap`: `dimension`（`yearByGroup`、`yearByStatus`）
- 既存の `progressSummary`、`achievementCards`、`groupProgress`、`statusMap`、`statusGrid`、`nextAchievements`、`itemList`

詳細画面の期間セレクターは「すべて」または年です。年別データは各項目の `firstVisitYear` に基づく初訪問データで、累積集計は選択年までの初訪問項目を数えます。実行コードや任意のクエリは受け付けません。データと合わない宣言はカタログ検証で拒否されます。

プラグインから任意のSwiftコード、JavaScript、外部クエリを実行することはできません。
