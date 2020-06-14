# Simple_Compiler

"コンピュータシステムの理論と実装"という本をもとにしてアセンブラとコンパイラーをPythonを使って構築しようという試み。
基本的には本の内容に忠実にPythonを使って実装をしている。本の中の機械語とオブジェクト指向言語のJackの仕様を流用している。

This project is tring to implement the assembler and compiler by Python based on the content of Japanese version of "The Elements of Computing Systems"(Noam Nisan, Shimon Schocken). In this project, Jack language and machine language of referenced book is used.

    * アセンブラは参考文献にある通り4つのモジュールに分割して実装した。参考文献内ではオブジェクト指向に近い形でパーサーのapiが提示されており、
    　イテレーターを実装するのが無難だと思われたが、できるだけ関数のみによって処理を記述したかったのでモジュール間のデータの共有には
      辞書のリストを使用している。ちなみにシンボルテーブルは専用のクラスを作ったが、Pythonの辞書で代用可能である。
    　Assembler is implemented in 4 modules as it is suggested in referenced book. In the book, Parser API was give as Object-Oriented 
      like pattern, and it looks like iterator should be used, however, since this project want to process the data as list, list of 
      dictionaly is used for the data trasfered between modules. SimbolTable is implemented as wrapper class of the dictionary, therefore,
      dictionary in Python can be directly used instead of this class.

    * VM変換器は基本的にはアセンブラと同じような構造となっている。ただし、コードライターは内部的に異なるアセンブリ言語のラベルを生成するために
      カウントを覚えておく必要があったため、関数ではなくクラスとして実装した。また変換器のメソッドはお互いにある程度独立しており、変換を完了
      するには全メソッドを順番に呼ぶ必要がある。
      The structure of VM translator is basically same with Assembler. However, CodeWriter is implemented as class, since it need to 
      record number of command called to generate the different Assembler Label. In addition, there is no one method which will translate
      the code at once. Instead of that, each methods have to be called in appropriate order.

Reference lists:  
コンピュータシステムの理論と実装 ―モダンなコンピュータの作り方　オライリージャパン (2015/3/25)