# smartkey
rasperry piでスマートロックを作成するためのもの
osはraspbian-stretch
slackbotをinstall
slackbot/plugins/__init__.py　空のファイルを別途作成

servo.pyはボタンでサーボを制御できるがpost.pyのほうでslack経由で制御すると変数の受け渡しを考慮しなくてもよいので楽
twitterにも投稿する用にしている。

* 2018/10/01 ファイル参照して変数を管理するように変更
