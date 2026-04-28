# 🎮 PyBreakout Academy: Game Design para Crianças

Este é um projeto educacional interativo desenvolvido em **Python** utilizando a biblioteca **Tkinter**. O objetivo é ensinar conceitos fundamentais de programação (Strings, Inteiros, Booleanos e Listas) para crianças de 8 a 12 anos, através da construção passo a passo de um jogo estilo *Breakout*.

---

## 🚀 Sobre o Projeto

O diferencial deste projeto é o seu **sistema de missões guiadas**. Ao invés de apenas jogar, o usuário assume o papel de um Game Designer e precisa "codificar" as propriedades do jogo para progredir. O tutor integrado valida o código em tempo real, fornecendo feedback visual e sonoro.

### 🛠️ Tecnologias Utilizadas
*   **Python 3.x**: Linguagem base.
*   **Tkinter**: Interface gráfica (GUI) e motor de renderização do jogo.
*   **Pygame (Mixer)**: Processamento de áudio e efeitos sonoros (SFX).
*   **Arquitetura Modular**: Separação por missões (`src/tutor/`) para facilitar a escalabilidade.

---

## 📋 Roadmap Pedagógico (As Missões)

O aprendizado é dividido em 5 etapas principais:

1.  **Missão 1: O Pintor de Mundos** 🎨  
2.  **Missão 2: Ferreiro de Raquetes** 🔨  
3.  **Missão 3: O Despertar da Bola** ⚽  
4.  **Missão 4: Física e Som** 🧱  
5.  **Missão 5: O Mestre do Código** 🏆  

---

## 🧠 Desafios Técnicos & Soluções

*   **Filtro de UX Dinâmico:** Trava lógica que impede o uso de cores que camuflariam os elementos.
*   **Gerenciamento de Estado do Canvas:** Verificações de segurança (`winfo_exists`) para evitar vazamento de memória entre missões.
*   **Feedback Educativo:** Sistema de validação visual e sonora que incentiva o aprendizado prático por tentativa e erro.

---

## 📦 Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/engsoftcris/breakout-academy-python.git](https://github.com/engsoftcris/breakout-academy-python.git)
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Inicie a academia:**
    ```bash
    python main.py
    ```

---

## 📚 Referências e Créditos

O desenvolvimento deste projeto foi inspirado em lógicas de jogos clássicos e recursos da comunidade:

*   **Lógica de Jogo:** Inspirado no tutorial da **MDN Web Docs**: *"2D breakout game using pure JavaScript"* — [Acessar Referência](https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript).
*   **Efeitos Sonoros:**
    *   *Clack 1.wav* por **radiohummingbird** — [Freesound.org](https://freesound.org/s/522956/) — Licença: **Attribution 4.0 (CC BY 4.0)**.
*   **Interface e Engine:** Adaptados e desenvolvidos em Python/Tkinter para fins educacionais.

---
Desenvolvido com ❤️ para a nova geração de programadores.