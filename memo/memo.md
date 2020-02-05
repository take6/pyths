# 自分用メモ

## 番組表取得先

Yahoo! Japanの番組表を使わせてもらう。

https://tv.yahoo.co.jp/listings


例えば、2020年2月1日の番組表は以下のURLから取得する

https://tv.yahoo.co.jp/listings?va=24&vd=0&d=20200201&a=23

ここで、

* `listings` - 地上波
    * 例えばBS1はここが`listings/bs1`になる
* `d=20200128`  - 日付
* `va=24`  - 24時間表示
* `a=23`  - 東京地域
* `vd=0`  - 番組詳細を表示しない


## 動的に生成されるwebページの内容を取得する

* webページの内容を取得して必要な情報を取り出すことを _スクレイピング_ というらしい。
* 必要なモジュールは、`selenium`
* `selenium`はブラウザ向けのドライバが必要なので別途インストールする必要がある
* Chromeを使うことにする

### `selenium`のインストール

```
$ pip install -U selenium
Collecting selenium
  Downloading selenium-3.141.0-py2.py3-none-any.whl (904 kB)
     |████████████████████████████████| 904 kB 1.2 MB/s
Requirement already satisfied, skipping upgrade: urllib3 in /Users/nakazato/pyvenv/SD/lib/python3.7/site-packages (from selenium) (1.25.8)
Installing collected packages: selenium
Successfully installed selenium-3.141.0
```

### Chromeのドライバインストール

[Seleniumのドキュメント][1]にしたがって、[Googleのダウンロードサイト][2]からダウンロード、インストールする。Chromeの現在のバージョンは`79.0.3945.130`なので、このバージョン向けのドライバをインストール。OSごとにzipファイルが用意されているので適切なものを選ぶ。zipを展開すると、`chromedriver`的な名前の実行ファイルが出てくるのでこれを`PATH`で認識できるようにする。

```
$ mv chromedriver $HOME/bin
$ which chromedriver
/Users/username/bin/chromedriver
```

[1]:https://selenium.dev/selenium/docs/api/py/index.html
[2]:https://sites.google.com/a/chromium.org/chromedriver/downloads

### 番組表の形式と欲しい情報

* 番組表は普通のテーブル: `<div id="tvpgm">`
* 番組名: `<td>`タグの値で、`<a href="..." class="title ...">タイトル</a>`の部分（`<wbr>`で区切られている）
* チャンネル: `<td>`タグの値で、`<a data-ylk="slk:tvttl; pos: N">`の`N`がチャンネル
* 放送開始時刻: `<td>`タグの値で、`<span class="time">HH:MM</span>` の部分
* 放送時間: `<td rowspan="x">` の `x` は分単位での放送時間
