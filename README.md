# Simple_Compiler

"コンピュータシステムの理論と実装"という本をもとにしてアセンブラとコンパイラーをPythonを使って構築しようという試み。
基本的には本の内容に忠実にPythonを使って実装をしている。本の中の機械語とオブジェクト指向言語のJackの仕様を流用している。

This project is tring to implement the assembler and compiler by Python based on the content of Japanese version of "The Elements of Computing Systems"(Noam Nisan, Shimon Schocken). In this project, Jack language and machine language of referenced book is used.

    * アセンブラは参考文献にある通り4つのモジュールに分割して実装した。参考文献内ではオブジェクト指向に近い形でapiが提示されており、イテレーターを
    　実装するのが無難だと思われたが、できるだけ関数のみによって処理を記述したかったのでモジュール間のデータの共有には辞書のリストを使用している。
    　Assembler is implemented in 4 modules as it is suggested in referenced book. In the book, API was give as Object-Oriented like pattern, 
      and it looks like iterator should be used, however, since this project want to process the data as list, list of dictionaly is used for 
      the data trasfered between modules.

Reference lists:  
コンピュータシステムの理論と実装 ―モダンなコンピュータの作り方　オライリージャパン (2015/3/25)