import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# Valores para o campo Código Vendedor
codigos_vendedor = ["128", "134", "135", "137", "149", "150", "156", "160", "161", "162", "165", "167", "171", "173", "176", "177", "182", "183", "184", "185", "220", "222", "223", "224", "225"]

# Variáveis para armazenar a tarefa em edição e motivos de observação
tarefa_em_edicao = None
motivos_obs = {} # Dicionário para rastrear os motivos de observação por tarefa

# Função para adicionar uma tarefa
def adicionar_tarefa():
    codigo_vendedor = codigo_vendedor_combobox.get()
    codigo_cliente = codigo_cliente_entry.get()
    razao_social = razao_social_entry.get()
    alteracao = alteracao_entry.get()
    prazo = prazo_entry.get()

    # Verifique se o campo "Código Cliente" está preenchido
    if not codigo_cliente:
        messagebox.showwarning("Campo Vazio", "O campo 'Código Cliente' deve ser preenchido.")
        return  # Sai da função se o campo "Código Cliente" estiver vazio

    # Se o campo "Código Cliente" estiver preenchido, prossiga com a adição da tarefa
    tarefa = (codigo_vendedor, codigo_cliente, razao_social, alteracao, prazo)
    tarefas_a_fazer.insert("", "end", values=tarefa)
    codigo_vendedor_combobox.set("")  # Limpa a seleção do combobox
    codigo_cliente_entry.delete(0, tk.END)
    razao_social_entry.delete(0, tk.END)
    alteracao_entry.delete(0, tk.END)
    prazo_entry.delete(0, tk.END)

# Função para editar a tarefa selecionada
def editar_tarefa():
    global tarefa_em_edicao
    selecao = tarefas_a_fazer.selection()
    if selecao:
        tarefa_em_edicao = selecao[0]
        valores_tarefa = tarefas_a_fazer.item(tarefa_em_edicao, "values")

        # Preencha os campos do formulário com os valores da tarefa selecionada
        codigo_vendedor_combobox.set(valores_tarefa[0])
        codigo_cliente_entry.delete(0, tk.END)
        codigo_cliente_entry.insert(0, valores_tarefa[1])
        razao_social_entry.delete(0, tk.END)
        razao_social_entry.insert(0, valores_tarefa[2])
        alteracao_entry.delete(0, tk.END)
        alteracao_entry.insert(0, valores_tarefa[3])
        prazo_entry.delete(0, tk.END)
        prazo_entry.insert(0, valores_tarefa[4])

# Função para salvar a edição da tarefa
def salvar_edicao():
    global tarefa_em_edicao
    if tarefa_em_edicao:
        nova_codigo_vendedor = codigo_vendedor_combobox.get()
        nova_codigo_cliente = codigo_cliente_entry.get()
        nova_razao_social = razao_social_entry.get()
        nova_alteracao = alteracao_entry.get()
        novo_prazo = prazo_entry.get()
        motivo_obs = motivos_obs.get(tarefa_em_edicao, "")  # Recupera o motivo de observação da tarefa em edição

        if motivo_obs:
            tarefas_a_fazer.item(tarefa_em_edicao, values=(nova_codigo_vendedor, nova_codigo_cliente, nova_razao_social, nova_alteracao, novo_prazo, motivo_obs), tags=("obs",))
        else:
            tarefas_a_fazer.item(tarefa_em_edicao, values=(nova_codigo_vendedor, nova_codigo_cliente, nova_razao_social, nova_alteracao, novo_prazo))

        # Limpa todos os campos do formulário
        codigo_vendedor_combobox.set("")
        codigo_cliente_entry.delete(0, tk.END)
        razao_social_entry.delete(0, tk.END)
        alteracao_entry.delete(0, tk.END)
        prazo_entry.delete(0, tk.END)

        tarefa_em_edicao = None


# Função para confirmar a alteração da tarefa
def confirmar_alteracao():
    global tarefa_em_edicao
    if tarefa_em_edicao:
        mensagem = f"A tarefa foi alterada com sucesso!"
        messagebox.showinfo("Alteração Confirmada", mensagem)
        salvar_edicao()

# Função para mover uma tarefa concluída
def concluir_tarefa():
    selecao = tarefas_a_fazer.selection()
    if selecao:
        tarefa = tarefas_a_fazer.item(selecao[0])['values']
        tarefas_a_fazer.delete(selecao)
        tarefas_concluidas.insert("", "end", values=tarefa)

# Função para mover uma tarefa de volta para tarefas a fazer
def voltar_tarefa():
    selecao = tarefas_concluidas.selection()
    if selecao:
        tarefa = tarefas_concluidas.item(selecao[0])['values']
        tarefas_concluidas.delete(selecao)
        tarefas_a_fazer.insert("", "end", values=tarefa)

# Função para imprimir tarefas concluídas
def imprimir_tarefas_concluidas():
    tarefas = tarefas_concluidas.get_children()
    if not tarefas:
        messagebox.showinfo("Tarefas Concluídas", "Não há tarefas concluídas para imprimir.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])

    if file_path:
        with open(file_path, "w") as file:
            for tarefa in tarefas:
                valores = tarefas_concluidas.item(tarefa)['values']
                file.write(f"Código Vendedor: {valores[0]}, Código Cliente: {valores[1]}, Razão Social: {valores[2]}, Alteração: {valores[3]}, Prazo: {valores[4]}\n")
        messagebox.showinfo("Tarefas Concluídas", f"Tarefas concluídas foram salvas em {file_path}")

# Função para marcar como observação
def marcar_como_obs():
    selecao = tarefas_a_fazer.selection()
    if selecao:
        item_selecionado = selecao[0]

        # Crie a janela de diálogo para inserir o motivo de observação
        obs_dialog = tk.Toplevel(root)
        obs_dialog.title("Motivo de Observação")

        motivo_obs_label = tk.Label(obs_dialog, text="Motivo da Observação:")
        motivo_obs_label.grid(row=0, column=0, sticky="w")

        motivo_obs_entry = tk.Entry(obs_dialog)
        motivo_obs_entry.grid(row=0, column=1)

        def salvar_motivo_obs():
            motivo_obs = motivo_obs_entry.get()
            if motivo_obs:
                # Atualize a tarefa com o motivo de observação
                tarefas_a_fazer.item(item_selecionado, values=(*tarefas_a_fazer.item(item_selecionado, "values"), motivo_obs), tags=("obs",))
                motivo_obs_entry.delete(0, tk.END)
                motivos_obs[item_selecionado] = motivo_obs
                obs_dialog.destroy()
                
        salvar_botao = tk.Button(obs_dialog, text="Salvar", command=salvar_motivo_obs)
        salvar_botao.grid(row=1, columnspan=2, padx=10, pady=10, sticky="ew")

# Configuração da janela principal
root = tk.Tk()
root.iconbitmap('icon.ico')

root.title("ALTERAÇÕES DIÁRIAS")

# Frame para o formulário de inclusão (à esquerda)
form_frame = tk.Frame(root)
form_frame.grid(row=0, column=0, padx=10, pady=10)

codigo_vendedor_label = tk.Label(form_frame, text="Código Vendedor:")
codigo_vendedor_label.grid(row=0, column=0, sticky="w")
codigo_vendedor_combobox = ttk.Combobox(form_frame, values=codigos_vendedor)
codigo_vendedor_combobox.grid(row=0, column=1)
codigo_vendedor_combobox.set("")  # Define uma seleção inicial vazia

codigo_cliente_label = tk.Label(form_frame, text="Código Cliente*:")
codigo_cliente_label.grid(row=1, column=0, sticky="w")
codigo_cliente_entry = tk.Entry(form_frame)
codigo_cliente_entry.grid(row=1, column=1)

razao_social_label = tk.Label(form_frame, text="Razão Social:")
razao_social_label.grid(row=2, column=0, sticky="w")
razao_social_entry = tk.Entry(form_frame)
razao_social_entry.grid(row=2, column=1)

alteracao_label = tk.Label(form_frame, text="Alteração:")
alteracao_label.grid(row=3, column=0, sticky="w")
alteracao_entry = tk.Entry(form_frame)
alteracao_entry.grid(row=3, column=1)

prazo_label = tk.Label(form_frame, text="Prazo:")
prazo_label.grid(row=4, column=0, sticky="w")
prazo_entry = tk.Entry(form_frame)
prazo_entry.grid(row=4, column=1)

# Botões para adicionar, editar, salvar e concluir tarefas (à direita do formulário)
adicionar_botao = tk.Button(root, text="Incluir Tarefa", command=adicionar_tarefa)
adicionar_botao.grid(row=0, column=1, padx=0, pady=0, sticky='ew')

editar_botao = tk.Button(root, text="Editar Tarefa", command=editar_tarefa)
editar_botao.grid(row=1, column=1, padx=0, pady=0, sticky='ew')

confirmar_alteracao_botao = tk.Button(root, text="Confirmar Alteração", command=confirmar_alteracao)
confirmar_alteracao_botao.grid(row=2, column=1, padx=0, pady=0, sticky='ew')



# Configuração da tabela de tarefas a fazer
tarefas_a_fazer = ttk.Treeview(root, columns=("Código Vendedor", "Código Cliente", "Razão Social", "Alteração", "Prazo"), show="headings")
tarefas_a_fazer.heading("Código Vendedor", text="VEN")
tarefas_a_fazer.heading("Código Cliente", text="COD CLI")
tarefas_a_fazer.heading("Razão Social", text="RAZÃO")
tarefas_a_fazer.heading("Alteração", text="ALTERAÇÃO")
tarefas_a_fazer.heading("Prazo", text="PRAZO")
tarefas_a_fazer.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

# Redimensão previa das colunas das taruefas a fazer
tarefas_a_fazer.column("Código Vendedor", width=30)
tarefas_a_fazer.column("Código Cliente", width=60)
tarefas_a_fazer.column("Razão Social", width=100)
tarefas_a_fazer.column("Alteração", width=350)
tarefas_a_fazer.column("Prazo", width=40)


# Configuração da tabela de tarefas concluídas
tarefas_concluidas = ttk.Treeview(root, columns=("Código Vendedor", "Código Cliente", "Razão Social", "Alteração", "Prazo"), show="headings")
tarefas_concluidas.heading("Código Vendedor", text="VEN")
tarefas_concluidas.heading("Código Cliente", text="COD CLI")
tarefas_concluidas.heading("Razão Social", text="RAZÃO")
tarefas_concluidas.heading("Alteração", text="ALTERAÇÃO")
tarefas_concluidas.heading("Prazo", text="PRAZO")
tarefas_concluidas.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

# Redimensão previa das colunas das tarefas concluídas
tarefas_concluidas.column("Código Vendedor", width=30)
tarefas_concluidas.column("Código Cliente", width=60)
tarefas_concluidas.column("Razão Social", width=100)
tarefas_concluidas.column("Alteração", width=350)
tarefas_concluidas.column("Prazo", width=40)

# Configuração das tags
tarefas_a_fazer.tag_configure("obs", background="green")
tarefas_concluidas.tag_configure("obs", background="green")

# Botão para Concluir tarefa
concluir_botao = tk.Button(root, text="Concluir Tarefa", command=concluir_tarefa)
concluir_botao.grid(row=5, column=0, padx=10, pady=10, sticky='ew')

# Botão para mover tarefa de volta para tarefas a fazer
voltar_botao = tk.Button(root, text="Voltar Tarefa", command=voltar_tarefa)
voltar_botao.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

# Botão para OBS
obs_botao = tk.Button(root, text="!", command=marcar_como_obs)
obs_botao.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

# Botão para imprimir tarefas concluídas (no rodapé)
imprimir_botao = tk.Button(root, text="Imprimir Tarefas Concluídas", command=imprimir_tarefas_concluidas)
imprimir_botao.grid(row=6, columnspan =2, padx=10, pady=10, sticky="ew")

# Configuração das colunas e linhas para expansão
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

def exibir_tarefa(event):
    item_selecionado = tarefas_a_fazer.selection()[0]
    valores_tarefa = tarefas_a_fazer.item(item_selecionado, "values")

    if len(valores_tarefa) >= 4:
        mensagem = f"Código Vendedor: {valores_tarefa[0]}\nCódigo Cliente: {valores_tarefa[1]}\nRazão Social: {valores_tarefa[2]}\nAlteração: {valores_tarefa[3]}\n"
    else:
        mensagem = ""

    if len(valores_tarefa) >= 5:
        mensagem += f"Prazo: {valores_tarefa[4]}\n"

    if len(valores_tarefa) > 5:
        mensagem += f"Motivo de Observação: {valores_tarefa[5]}"
    
    messagebox.showinfo("Detalhes da Tarefa", mensagem)

tarefas_a_fazer.bind("<Double-1>", exibir_tarefa)

root.mainloop()