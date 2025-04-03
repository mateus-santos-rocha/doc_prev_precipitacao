import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def plot_radar(df,
               label, 
               value,
               hue=None, 
               figsize=(6,6), 
               title="Gráfico de Radar", 
               title_font_color='black',
               title_font_size=15,
               title_pad=20,
               plot_colors=['blue', 'red', 'green', 'purple', 'orange'],
               labels_font_color='darkblue',
               labels_font_size=12,
               display_values=True,
               values_font_color='green',
               values_font_size=10,
               values_offset=0.25,
               fill_alpha=0.25):
    
    labels = list(df[label].unique())
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Fechar o gráfico
    
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))
    ax.set_title(title, size=title_font_size, color=title_font_color, pad=title_pad)
    
    if hue:
        hues = df[hue].unique()
        for i, h in enumerate(hues):
            hue_df = df[df[hue] == h]
            hue_values = list(hue_df[value]) + [hue_df[value].iloc[0]]
            color = plot_colors[i % len(plot_colors)]
            
            ax.fill(angles, hue_values, color=color, alpha=fill_alpha)
            ax.plot(angles, hue_values, color=color, linewidth=2, label=f'{hue}: {h}')
            
            if display_values:
                for angle, val in zip(angles, hue_values):
                    ax.text(angle, val + values_offset, f'{val:.2f}', ha='center', va='center',
                            fontsize=values_font_size, color=values_font_color)
        
        ax.legend(bbox_to_anchor=(1.1, 1.05))
    else:
        values = list(df[value]) + [df[value].iloc[0]]
        ax.fill(angles, values, color=plot_colors[0], alpha=fill_alpha)
        ax.plot(angles, values, color=plot_colors[0], linewidth=2)
        
        if display_values:
            for angle, value in zip(angles, values):
                ax.text(angle, value + values_offset, f'{value:.2f}', ha='center', va='center',
                        fontsize=values_font_size, color=values_font_color)
    
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color=labels_font_color, size=labels_font_size)

    plt.show()


def comparar_prototipos_metricas_basicas(metrics_list,titles_list):
    prototipo_dict = {titles_list[i]:prototipo for i,prototipo in enumerate(metrics_list)}
    prototipo = pd.melt(pd.concat({k: pd.DataFrame(v).T for k, v in prototipo_dict.items()}, axis=0).reset_index(names=['Protótipo','Modelo']),id_vars=['Protótipo','Modelo'],var_name='Métrica',value_name='Score')
    
    # Configurar o tamanho da figura e número de subplots (1 linha, 2 colunas)
    models = list(metrics_list[0].keys())
    fig, axes = plt.subplots(1, len(models), figsize=(14, 6))

    for i,model in enumerate(models,1):
        g = sns.barplot(data=prototipo.loc[prototipo['Modelo'] == model], hue='Protótipo', x='Métrica', y='Score', ax=axes[i-1])
        for j in g.containers:
            g.bar_label(j,fmt='%.2f')
        axes[i-1].set_title(f'Modelo {model}')
        axes[i-1].grid()
        axes[i-1].set_axisbelow(True)
        axes[i-1].set_ylim(-0.5,10)
    # Ajuste da legenda para não sobrepor
    plt.tight_layout()
    plt.show()

def comparar_prototipos_sem_chuva(predictions_list,titles_list,threshold_mm=0.5):
    predictions_dict = {titles_list[i]:prototipo for i,prototipo in enumerate(predictions_list)}

    sem_chuva = {
        prototipo:{
            model:df.loc[df['y_test']==0] for model,df in prediction.items()}
        for prototipo,prediction in predictions_dict.items()}

    acerto = {
        prototipo: {
            model:len(df.loc[df['y_pred']==0])*100/len(df) for model,df in prediction.items()}
        for prototipo,prediction in sem_chuva.items()
    }

    proximo = {
        prototipo: {
            model:len(df.loc[df['y_pred']<=threshold_mm])*100/len(df) for model,df in prediction.items()}
        for prototipo,prediction in sem_chuva.items()
    }

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))


    plot_df_exato = pd.melt(pd.DataFrame(acerto).reset_index(names='Modelo'),id_vars='Modelo',value_name='% Acerto 0mm')
    g = sns.barplot(data=plot_df_exato,x='Modelo',hue='variable',y='% Acerto 0mm',ax=axes[0])
    for j in g.containers:
            g.bar_label(j,fmt='%.1f%%')
    axes[0].set_title('Previsão sem chuva - Acerto exato')
    axes[0].grid()
    axes[0].set_axisbelow(True)
    axes[0].set_ylim(0,100)

    plot_df_aproximado = pd.melt(pd.DataFrame(proximo).reset_index(names='Modelo'),id_vars='Modelo',value_name=f'% Previsão menos de {threshold_mm}mm')
    g = sns.barplot(data=plot_df_aproximado,x='Modelo',hue='variable',y=f'% Previsão menos de {threshold_mm}mm',ax=axes[1])
    for j in g.containers:
            g.bar_label(j,fmt='%.1f%%')
    axes[1].set_title('Previsão sem chuva - Acerto aproximado')
    axes[1].grid()
    axes[1].set_axisbelow(True)
    axes[1].set_ylim(0,100)

    plt.tight_layout()
    plt.show()

def comparar_prototipos_com_chuva(predictions_list,titles_list,threshold_mm_1,threshold_mm_2):
    predictions_dict = {titles_list[i]:prototipo for i,prototipo in enumerate(predictions_list)}

    com_chuva = {
        prototipo:{
            model:df.loc[df['y_test']>0] for model,df in prediction.items()}
        for prototipo,prediction in predictions_dict.items()}

    proximo_1 = {
        prototipo: {
            model:len(df.loc[(df['y_pred']-df['y_test']).abs()<=threshold_mm_1])*100/len(df) for model,df in prediction.items()}
        for prototipo,prediction in com_chuva.items()
    }

    proximo_2 = {
        prototipo: {
            model:len(df.loc[(df['y_pred']-df['y_test']).abs()<=threshold_mm_2])*100/len(df) for model,df in prediction.items()}
        for prototipo,prediction in com_chuva.items()
    }

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))


    plot_df_proximo_1 = pd.melt(pd.DataFrame(proximo_1).reset_index(names='Modelo'),id_vars='Modelo',value_name=f'% Acerto com erro de até {threshold_mm_1}mm')
    g = sns.barplot(data=plot_df_proximo_1,x='Modelo',hue='variable',y=f'% Acerto com erro de até {threshold_mm_1}mm',ax=axes[0])
    for j in g.containers:
            g.bar_label(j,fmt='%.1f%%')
    axes[0].set_title(f'Previsão com chuva - Acerto com erro de até {threshold_mm_1}mm')
    axes[0].grid()
    axes[0].set_axisbelow(True)
    axes[0].set_ylim(0,100)

    plot_df_proximo_2 = pd.melt(pd.DataFrame(proximo_2).reset_index(names='Modelo'),id_vars='Modelo',value_name=f'% Acerto com erro de até {threshold_mm_2}mm')
    g = sns.barplot(data=plot_df_proximo_2,x='Modelo',hue='variable',y=f'% Acerto com erro de até {threshold_mm_2}mm',ax=axes[1])
    for j in g.containers:
            g.bar_label(j,fmt='%.1f%%')
    axes[1].set_title(f'Previsão com chuva - Acerto com erro de até {threshold_mm_2}mm')
    axes[1].grid()
    axes[1].set_axisbelow(True)
    axes[1].set_ylim(0,100)

    plt.tight_layout()
    plt.show()

def comparar_prototipos_com_muita_chuva(predictions_list,titles_list,threshold_muita_chuva_mm,threshold_mm_1,threshold_mm_2):
    predictions_dict = {titles_list[i]:prototipo for i,prototipo in enumerate(predictions_list)}

    com_chuva = {
        prototipo:{
            model:df.loc[df['y_test']>threshold_muita_chuva_mm] for model,df in prediction.items()}
        for prototipo,prediction in predictions_dict.items()}

    proximo_1 = {
        prototipo: {
            model:len(df.loc[(df['y_pred']-df['y_test']).abs()<=threshold_mm_1])*100/len(df) for model,df in prediction.items()}
        for prototipo,prediction in com_chuva.items()
    }

    proximo_2 = {
        prototipo: {
            model:len(df.loc[(df['y_pred']-df['y_test']).abs()<=threshold_mm_2])*100/len(df) for model,df in prediction.items()}
        for prototipo,prediction in com_chuva.items()
    }

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))


    plot_df_proximo_1 = pd.melt(pd.DataFrame(proximo_1).reset_index(names='Modelo'),id_vars='Modelo',value_name=f'% Acerto com erro de até {threshold_mm_1}mm')
    g = sns.barplot(data=plot_df_proximo_1,x='Modelo',hue='variable',y=f'% Acerto com erro de até {threshold_mm_1}mm',ax=axes[0])
    for j in g.containers:
            g.bar_label(j,fmt='%.1f%%')
    axes[0].set_title(f'Previsão com chuva de mais de {threshold_muita_chuva_mm}mm - Acerto com erro de até {threshold_mm_1}mm')
    axes[0].grid()
    axes[0].set_axisbelow(True)
    axes[0].set_ylim(0,100)

    plot_df_proximo_2 = pd.melt(pd.DataFrame(proximo_2).reset_index(names='Modelo'),id_vars='Modelo',value_name=f'% Acerto com erro de até {threshold_mm_2}mm')
    g = sns.barplot(data=plot_df_proximo_2,x='Modelo',hue='variable',y=f'% Acerto com erro de até {threshold_mm_2}mm',ax=axes[1])
    for j in g.containers:
            g.bar_label(j,fmt='%.1f%%')
    axes[1].set_title(f'Previsão com chuva de mais de {threshold_muita_chuva_mm}mm - Acerto com erro de até {threshold_mm_2}mm')
    axes[1].grid()
    axes[1].set_axisbelow(True)
    axes[1].set_ylim(0,100)

    plt.tight_layout()
    plt.show()
