
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def annotating_plots(ax = None, formatter = None, orientation = 'v', stacked = False, kind = 'bar', 
                     fontsize = 12, colors = None, weight='medium', rotation = 0, total=False):
    if ax is None:
        # axisが指定されていない場合、現在描画されているオブジェクトから取得する
        ax = plt.gca()

    if formatter is None:
        #デフォルトでは、数値をそのまま文字列として出力する
        formatter = lambda x : str(x)

    elif formatter == 'percent':
        # データラベルの表現が文字列でpercentと指定された場合、formatterを設定する
        formatter = lambda x : '{:.{}f}%'.format(x*100, 1)


    if colors is None:
        # 色が指定されていない場合、全て黒にする
        colors = ['black' for _ in range(len(ax.patches))]

    elif isinstance(colors, str):
        if colors != 'auto':
            # 色が文字列で指定されている場合、これを全てのデータラベルにブロードキャストする
            colors = [colors for _ in range(len(ax.patches))]

        else:
            #colors = 'auto'は、Stacked bar向けのオプション。rgbを輝度に変換し、0.5以下なら白字にする
            colors = ['white' if np.dot([0.3, 0.6, 0.1],p.get_facecolor()[:3]) <= 0.5 else 'black' for p in ax.patches]


    if kind == 'bar':
        # 棒グラフの場合
        if orientation == 'v':
            if not stacked:
                # Grouped bar
                for cnt, p in enumerate(ax.patches):
                    ax.annotate(formatter(p.get_height()),
                                (p.get_x() + p.get_width()/2, p.get_height()*1.005),
                                ha='center', 
                                va='bottom',
                                fontsize=fontsize,
                                color = colors[cnt],
                                weight = weight,
                                rotation = rotation
                                )

            else:
                # Stacked barはoffsetが必要なため、offsetデータ格納用配列を定義する
                length = pd.Series([p.get_x() for p in ax.patches]).nunique() #axisの長さ
                offset = np.zeros(length)
                for cnt, p in enumerate(ax.patches):
                    ax.annotate(formatter(p.get_height()),
                                (p.get_x() + p.get_width()/2, p.get_height()/2 + offset[cnt%length]),
                                horizontalalignment='center',
                                verticalalignment='center',
                                color = colors[cnt],
                                size = fontsize,
                                weight = weight,
                                rotation = rotation
                                )
                    offset[cnt%length] += p.get_height()
                if total:
                    # Stacked barに対し、合計値を表示
                    for idx, p in zip(range(length), ax.patches):
                        ax.annotate(formatter(offset[idx]), 
                                    (p.get_x() + p.get_width()/2, offset[idx]),
                                    horizontalalignment='center',
                                    verticalalignment='bottom',
                                    weight = weight,
                                    rotation = rotation
                                    )               

        elif orientation == 'h':
            if not stacked:
                for cnt, p in enumerate(ax.patches):
                    ax.annotate(formatter(p.get_width()),
                                (p.get_width(),p.get_y() + p.get_height()/2),
                                horizontalalignment='left',
                                verticalalignment='center',
                                fontsize=fontsize,
                                color = colors[cnt],
                                weight = weight,
                                rotation = rotation
                                )

            else:
                # Stacked barはoffsetが必要なため、offsetデータ格納用配列を定義する
                length = pd.Series([p.get_y() for p in ax.patches]).nunique() #axisの長さ
                offset = np.zeros(length)
                for cnt, p in enumerate(ax.patches):
                    ax.annotate(formatter(p.get_width()),
                                (p.get_width()/2 + offset[cnt%length], p.get_y() + p.get_height()/2),
                                horizontalalignment='center',
                                verticalalignment='center',
                                color = colors[cnt],
                                size = fontsize,
                                weight = weight,
                                rotation = rotation
                                )
                    offset[cnt%length] += p.get_width()
                if total:
                    # Stacked barに対し、合計値を表示
                    for idx, p in zip(range(length), ax.patches):
                        ax.annotate(formatter(offset[idx]), 
                                    (offset[idx],
                                    p.get_y() + p.get_height()/2),
                                    horizontalalignment='left',
                                    verticalalignment='center',
                                    weight = weight,
                                    rotation = rotation
                                    )


# In[ ]:



