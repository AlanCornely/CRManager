# CRM COM GESTÃO DE ESTOQUE - CRManager

**Autor:** Alan M. Cornely

**Data:** 25 de Novembro de 2025

**Versão:** 1.0

---

## 1. Introdução e Visão Geral

Este documento define o escopo do projeto para o desenvolvimento de um **Sistema de CRM (Customer Relationship Management) com Foco em Gestão de Estoque**. O objetivo principal é integrar as funcionalidades de relacionamento com o cliente com a gestão eficiente do inventário, permitindo uma visão unificada e estratégica das operações de vendas e logística.

O sistema visa otimizar processos, reduzir erros de estoque, melhorar a precisão das previsões de vendas e, consequentemente, aumentar a satisfação do cliente e a rentabilidade da empresa.

### Problemas que o sistema resolve:
*   Falta de controle de entradas/saídas de estoque.
*   Integração ruim entre vendas e estoque.
*   Dificuldade em rastrear produtos, pedidos e clientes.

### Público-alvo:
Empresas que vendem produtos físicos (lojas, distribuidoras, e-commerce, etc.).

---
## 2. Objetivos e Critérios de Sucesso

| Categoria | Objetivo | Descrição | Critério de Sucesso |
| :--- | :--- | :--- | :--- |
| **Gestão de Estoque** | Otimização do Inventário | Reduzir o excesso de estoque e a falta de produtos (ruptura), garantindo níveis ideais. | Redução de **90%** nas divergências de estoque identificadas durante os inventários físicos. |
| **Relacionamento com o Cliente** | Visão 360º do Cliente | Centralizar todas as interações e histórico de pedidos do cliente para um atendimento personalizado. | O CRM deve armazenar **histórico de contato** e **histórico de compras** para todos os clientes. |
| **Processos** | Automação de Fluxos | Automatizar a atualização de estoque após vendas e a geração de alertas de reabastecimento. | Redução de **20%** no tempo gasto pela equipe de vendas para processar um pedido. |
| **Tomada de Decisão** | Relatórios e Análises | Fornecer dados em tempo real sobre o desempenho de vendas, giro de estoque e lucratividade por produto/cliente. | Todos os relatórios devem exportar para **PDF/Excel**. |

---

## 3. Funcionalidades Chave (Módulos Principais)

### 3.1. Módulo de Clientes (CRM)
*   **Cadastro Completo:** Clientes (empresa/pessoa), armazenamento de dados de contato e preferências.
*   **Histórico:** Histórico de compras e histórico de atendimento.
*   **Comunicação:** Registro de contato (ligações, WhatsApp, e-mails) e notas de reuniões.
*   **Funil de Vendas:** Rastreamento do pipeline (Prospecção → Contato → Proposta → Negociação → Fechamento).
*   **Gestão de Oportunidades:** Rastreamento do pipeline de vendas, desde o lead até a conversão.
*   **Agendamento e Lembretes** (follow-up).
*   **Análise de Clientes:** Ticket médio, produtos mais comprados, perfil de compra.

### 3.2. Módulo de Produtos
*   **Cadastro Detalhado:** SKU/código interno, nome, descrição, unidade de medida, fornecedor, preço de custo e venda, categoria.
*   **Variações:** Cadastro de variações (tamanho, cor, modelo).
*   **Mídia:** Fotos e documentos anexos.

### 3.3. Módulo de Estoque (Inventário)
*   **Movimentação:** Registro de Entradas (compra, devolução, ajuste) e Saídas (venda, consumo interno, perda).
*   **Detalhes da Movimentação:** Movimentações detalhadas com data, usuário e motivo.
*   **Localização:** Controle de múltiplos depósitos/locais (armazéns, corredores, prateleiras).
*   **Controle de Nível:** Mínimo e máximo por produto.
*   **Alertas:** Alerta de reposição automática (estoque mínimo).
*   **Inventário Físico:** Ferramenta para contagem e ajuste de estoque, com registro de Divergências (esperado vs. encontrado).

### 3.4. Módulo de Pedidos / Vendas
*   **Criação:** Criação de orçamentos e conversão para pedido.
*   **Disponibilidade:** Consulta em tempo real da disponibilidade de estoque.
*   **Reserva de Estoque:** Capacidade de reservar itens para pedidos em andamento ou cotações.
*   **Baixa Automática:** Baixa automática após venda.
*   **Faturamento:** Emissão de nota fiscal (se aplicável) e integração com faturamento.
*   **Status do Pedido:** Em análise, Aprovado, Separação, Enviado, Concluído.

### 3.5. Módulo de Fornecedores
*   **Cadastro:** Cadastro de fornecedores.
*   **Histórico:** Histórico de compras.
*   **Performance:** Análise de performance (prazo, preço, qualidade).
*   **Pedidos de Compra:** Cotação, Aprovação, Recebimento e Baixa automática no estoque.

### 3.6. Módulo Financeiro (Opcional/Básico)
*   Contas a pagar (ligado à compra).
*   Contas a receber (ligado às vendas).
*   Relatórios financeiros básicos.
*   Conciliação básica.
*   *Nota: Funcionalidades avançadas de contabilidade e folha de pagamento estão **fora do escopo**.*

### 3.7. Dashboard e Relatórios
*   **Dashboard:** Nível de estoque, Ações pendentes, Funil de vendas, Acompanhar histórico do cliente.
*   **Relatórios Principais:** Ruptura de estoque, Curva ABC de produtos, Produtos mais vendidos, Estoque parado, Vendas por cliente, Projeção de compras, Comparativo de preços, Giro de Estoque, Previsão de Demanda (básica).

---

## 4. Fluxos de Trabalho (Workflows) e Regras de Negócio

### 4.1. Fluxos de Trabalho
*   **Fluxo de Venda:** Cliente cria pedido → Estoque reserva item → Pedido aprovado → Estoque dá baixa → Entrega → Registro no CRM.
*   **Fluxo de Compra:** Solicitação → Cotação → Pedido → Recebimento → Entrada no estoque.

### 4.2. Regras de Negócio
*   Produtos **não podem** ficar com estoque negativo.
*   Venda só acontece se houver **quantidade mínima** disponível.
*   Cada usuário só pode editar o que estiver dentro do seu **nível de permissão**.
*   Histórico **não pode ser apagado** (apenas inativado).
*   Cada movimentação deve registrar **usuário, data e motivo**.

---

## 5. Requisitos Técnicos e Não Funcionais

| Tipo | Requisito | Detalhe |
| :--- | :--- | :--- |
| **Tecnologia** | Stack de Desenvolvimento | Python (ou Node.js), Vue e MySQL. |
| **Backend** | Arquitetura | python (talvez node) |
| **Frontend** | Arquitetura | vue |
| **Banco de Dados** | Armazenamento | MySQL |
| **Autenticação** | Acesso | JWT, OAuth, Autenticação de dois fatores (2FA) opcional. |
| **Segurança** | Proteção de Dados | Criptografia SSL/TLS, Criptografia de dados sensíveis, Conformidade com LGPD, Backup automático. |
| **API** | Integração Externa | API REST pública para comunicação com outros sistemas. |
| **Controle** | Logs | Logs de alteração e Permissões/Níveis de acesso. |
| **Performance** | Tempo de Resposta | O tempo de carregamento de páginas e relatórios críticos não deve exceder **3 segundos**. |
| **Disponibilidade** | Uptime | O sistema deve ter uma disponibilidade mínima de **99,5%**. |
| **Usabilidade** | Interface | A interface deve ser limpa, intuitiva e responsiva (desktop e mobile via navegador). |

---

## 6. Escopo Fora do Projeto (Out-of-Scope)

É importante definir o que o projeto **não** irá contemplar para evitar desvios de escopo:
*   **Integração com Sistemas Externos:** Não inclui integração nativa com ERPs, sistemas de contabilidade ou plataformas de e-commerce de terceiros (a API REST pública será o ponto de integração).
*   **Módulo Financeiro Completo:** Não inclui funcionalidades avançadas de contas a pagar/receber, conciliação bancária ou folha de pagamento.
*   **Logística e Rastreamento de Entregas:** Não inclui gestão de frota, roteirização ou rastreamento em tempo real de transportadoras.
*   **Análise Preditiva Avançada:** A previsão de demanda será básica (baseada em médias históricas), sem uso de modelos complexos de Machine Learning.
*   **PDV** (ponto de venda).
*   **Gestão fiscal avançada.**
*   **Funcionalidades industriais** (BOM, produção, etc.).

---

## 7. Cronograma e Próximos Passos

### Fases do Projeto:
1.  Levantamento e prototipação (incluindo a aprovação formal deste escopo).
2.  Arquitetura do sistema e especificações técnicas detalhadas (*wireframes*).
3.  Desenvolvimento por módulos.
4.  Testes.
5.  Treinamento para usuários-chave e documentação de uso.
6.  Implantação.
7.  Suporte pós-lançamento.

### Próximos Passos Imediatos:
1.  **Aprovação do Escopo:** Revisão e aprovação formal deste documento pelas partes interessadas.
2.  **Levantamento Detalhado:** Criação de *wireframes* e especificações técnicas detalhadas para cada funcionalidade.
3.  **Planejamento:** Definição do cronograma, alocação de recursos e estimativa de custos.
4.  **Desenvolvimento:** Início da fase de codificação e testes.
