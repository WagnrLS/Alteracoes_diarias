import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# Valores para o campo Código Vendedor
codigos_vendedor = ["128", "134", "135", "137", "149", "150", "156", "160", "161", "162", "165", "167", "171", "173", "176", "177", "182", "183", "184", "185", "220", "222", "223", "224", "225"]

# Variáveis para armazenar a tarefa em edição
tarefa_em_edicao = None

# Função para adicionar uma tarefa
def adicionar_tarefa():
    codigo_vendedor = codigo_vendedor_combobox.get()
    codigo_cliente = codigo_cliente_entry.get()
    razao_social = razao_social_entry.get()
    alteracao = alteracao_entry.get()

    # Verifique se todos os campos estão preenchidos
    if codigo_vendedor and codigo_cliente and razao_social and alteracao:
        tarefa = (codigo_vendedor, codigo_cliente, razao_social, alteracao)
        tarefas_a_fazer.insert("", "end", values=tarefa)
        codigo_vendedor_combobox.set("")  # Limpa a seleção do combobox
        codigo_cliente_entry.delete(0, tk.END)
        razao_social_entry.delete(0, tk.END)
        alteracao_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Campos Vazios", "Preencha todos os campos!")

# Função para editar a tarefa selecionada
def editar_tarefa():
    global tarefa_em_edicao
    selecao = tarefas_a_fazer.selection()
    if selecao:
        tarefa_em_edicao = selecao[0]
        alteracao_atual = tarefas_a_fazer.item(tarefa_em_edicao, "values")[3]
        alteracao_entry.delete(0, tk.END)
        alteracao_entry.insert(0, alteracao_atual)

# Função para salvar a edição da tarefa
def salvar_edicao():
    global tarefa_em_edicao
    if tarefa_em_edicao:
        nova_alteracao = alteracao_entry.get()
        tarefas_a_fazer.item(tarefa_em_edicao, values=(tarefas_a_fazer.item(tarefa_em_edicao, "values")[0],
                                                       tarefas_a_fazer.item(tarefa_em_edicao, "values")[1],
                                                       tarefas_a_fazer.item(tarefa_em_edicao, "values")[2],
                                                       nova_alteracao))
        alteracao_entry.delete(0, tk.END)
        tarefa_em_edicao = None

# Função para confirmar a alteração da tarefa
def confirmar_alteracao():
    global tarefa_em_edicao
    if tarefa_em_edicao:
        mensagem = f"A tarefa foi alterada para:\n{alteracao_entry.get()}"
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
                file.write(f"Código Vendedor: {valores[0]}, Código Cliente: {valores[1]}, Razão Social: {valores[2]}, Alteração: {valores[3]}\n")
        messagebox.showinfo("Tarefas Concluídas", f"Tarefas concluídas foram salvas em {file_path}")

# Configuração da janela principal
root = tk.Tk()
root.title("Sistema Gerenciador de Tarefas")

# Frame para o formulário de inclusão (à esquerda)
form_frame = tk.Frame(root)
form_frame.grid(row=0, column=0, padx=10, pady=10)

codigo_vendedor_label = tk.Label(form_frame, text="Código Vendedor:")
codigo_vendedor_label.grid(row=0, column=0, sticky="w")
codigo_vendedor_combobox = ttk.Combobox(form_frame, values=codigos_vendedor)
codigo_vendedor_combobox.grid(row=0, column=1)
codigo_vendedor_combobox.set("")  # Define uma seleção inicial vazia

codigo_cliente_label = tk.Label(form_frame, text="Código Cliente:")
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

# Botões para adicionar, editar, salvar e concluir tarefas (à direita do formulário)
adicionar_botao = tk.Button(root, text="Incluir Tarefa", command=adicionar_tarefa)
adicionar_botao.grid(row=0, column=1, padx=0, pady=0, sticky='ew')

editar_botao = tk.Button(root, text="Editar Tarefa", command=editar_tarefa)
editar_botao.grid(row=1, column=1, padx=0, pady=0, sticky='ew')

confirmar_alteracao_botao = tk.Button(root, text="Confirmar Alteração", command=confirmar_alteracao)
confirmar_alteracao_botao.grid(row=2, column=1, padx=0, pady=0, sticky='ew')



# Configuração da tabela de tarefas a fazer
tarefas_a_fazer = ttk.Treeview(root, columns=("Código Vendedor", "Código Cliente", "Razão Social", "Alteração"), show="headings")
tarefas_a_fazer.heading("Código Vendedor", text="Código Vendedor")
tarefas_a_fazer.heading("Código Cliente", text="Código Cliente")
tarefas_a_fazer.heading("Razão Social", text="Razão Social")
tarefas_a_fazer.heading("Alteração", text="Alteração")
tarefas_a_fazer.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

# Configuração da tabela de tarefas concluídas
tarefas_concluidas = ttk.Treeview(root, columns=("Código Vendedor", "Código Cliente", "Razão Social", "Alteração"), show="headings")
tarefas_concluidas.heading("Código Vendedor", text="Código Vendedor")
tarefas_concluidas.heading("Código Cliente", text="Código Cliente")
tarefas_concluidas.heading("Razão Social", text="Razão Social")
tarefas_concluidas.heading("Alteração", text="Alteração")
tarefas_concluidas.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

# Botão para Concluir tarefa
concluir_botao = tk.Button(root, text="Concluir Tarefa", command=concluir_tarefa)
concluir_botao.grid(row=5, column=0, padx=10, pady=10, sticky='ew')

# Botão para mover tarefa de volta para tarefas a fazer
voltar_botao = tk.Button(root, text="Voltar Tarefa", command=voltar_tarefa)
voltar_botao.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

# Botão para imprimir tarefas concluídas (no rodapé)
imprimir_botao = tk.Button(root, text="Imprimir Tarefas Concluídas", command=imprimir_tarefas_concluidas)
imprimir_botao.grid(row=6, columnspan=2, padx=10, pady=10, sticky="ew")

# Configuração das colunas e linhas para expansão
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
