# %%
import time
import pandas as pd
from sqlalchemy import create_engine
import os
import asyncio
import matplotlib.pyplot as plt
# import psycopg2
import seaborn as sns


async def main():
    # INPUT YOUR OWN CONNECTION STRING HERE
    conn_string = 'postgresql://postgres:yourpass@localhost:5432/enem'

    db = create_engine(conn_string)
    conn = db.connect()
    start_time = time.time()

    df = pd.read_sql_query('select tfrf.ds_faixa_renda_familiar as rendaFamiliar, avg(tpo.nu_nota) as nota, stddev(tpo.nu_nota) as desviopadrao from tb_participante tp \
            inner join tb_questionario_socioeconomico tqs on  tqs.nu_inscricao_participante = tp.nu_inscricao_participante \
	        inner join tb_faixa_renda_familiar tfrf on  tfrf.id_faixa_renda_familiar = tqs.cd_faixa_renda_familiar \
	        inner join  tb_prova_objetiva tpo on  tpo.nu_inscricao_participante  = tp.nu_inscricao_participante \
	        group by tfrf.ds_faixa_renda_familiar \
	        order by tfrf.ds_faixa_renda_familiar', con=conn)

    # print(df.columns)
    # print(df.dtypes)
    print(df)
    # plt.figure()

    # df.iloc[2].plot.bar()
    # df.iloc['avg'].plot.bar()

    # plt.axhline(0, color="k")

    x_axis = df["desviopadrao"]
    y_axis = df["nota"]

    sns.set_theme()
    sns.scatterplot(x=x_axis, y=y_axis, hue=df.rendafamiliar, s=200)
    plt.title("Notas pelo grupo de ocupação da figura paterna - ENEM 2021")
    # sns.boxplot(data=df, x='avg', y='stddev')

    # sns.pairplot(data=df,  hue="rendafamiliar")

    plt.show()

    conn.close()

    print("End of selecting")
    # time.sleep(10)
asyncio.run(main())


# select tfrf.ds_faixa_renda_familiar, avg(tpo.nu_nota), stddev(tpo.nu_nota)
# 	 from tb_participante tp
# 	 inner join tb_questionario_socioeconomico tqs on  tqs.nu_inscricao_participante = tp.nu_inscricao_participante
# 	 inner join tb_faixa_renda_familiar tfrf on  tfrf.id_faixa_renda_familiar = tqs.cd_faixa_renda_familiar
# 	 inner join  tb_prova_objetiva tpo on  tpo.nu_inscricao_participante  = tp.nu_inscricao_participante
# 	 group by tfrf.ds_faixa_renda_familiar
# 	 order by tfrf.ds_faixa_renda_familiar
