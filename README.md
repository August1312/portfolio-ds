# Portfólio DS

Portfolio pessoal desenvolvido com Django, estilizado com CSS moderno, navegação responsiva e otimizado para SEO/social sharing.

## Visão Geral

Este projeto é um portfólio profissional para apresentar:
- perfil do desenvolvedor
- competências e áreas de atuação
- projetos
- contato
- analytics

A interface foi pensada para um visual tecnológico, com destaque em azul escuro, verde vibrante e elementos modernos.

## Tecnologias Utilizadas

- Python
- Django 6.0.7
- SQLite
- HTML
- CSS
- JavaScript
- Font Awesome
- Google Fonts

## Estrutura do Projeto

```text
portfolio-ds/
├── core/
│   ├── templates/
│   ├── static/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── portfolio/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
└── requirements.txt
```

## Funcionalidades Implementadas

### 1. Página Home
- Hero section com layout centralizado
- Botões principais "Ver Projetos" e "Entre em Contato"
- Ícones de papéis com destaque visual
- Background tecnológico com gradiente e brilho
- Comportamento responsivo em celular

### 2. Navbar
- Posicionamento fixo no topo
- Logo destacado como "DS"
- Links com ícones lineares
- Destaque visual do item ativo
- Hover com underline animado
- Versão mobile com botão hambúrguer
- Efeito de slide suave e transição visual

### 3. Estilo Visual
- Paleta com fundo azul escuro e acentos verdes
- Tipografia com Inter e Roboto
- Botões com gradiente e sombra suave
- Blocos com cards, elevadores visuais e contraste aprimorado

### 4. SEO e Social Sharing
- Meta tags Open Graph
- Meta tags para Twitter Card
- Canonical URL
- Favicon SVG
- robots.txt
- sitemap.xml
- URLs públicas configuradas para indexação

## SEO Implementado

### Open Graph
A página utiliza meta tags para melhorar a aparência ao compartilhar links em redes sociais, incluindo:
- `og:title`
- `og:description`
- `og:image`
- `og:url`

### Canonical
A URL canônica foi configurada no template base com `rel="canonical"` para reduzir duplicação de conteúdo.

### Sitemap
O arquivo `sitemap.xml` foi criado contendo as páginas principais do portfólio.

### Robots
O arquivo `robots.txt` foi adicionado para orientar motores de busca.

## Arquivos de SEO e Ícones

- `core/templates/base.html` → meta tags, favicon, canonical
- `core/templates/sitemap.xml` → sitemap do site
- `core/templates/robots.txt` → regras de rastreamento
- `core/static/images/favicon.svg` → ícone principal do site

## Segurança e Git

Este projeto já possui um arquivo `.gitignore` preparado para proteger informações sensíveis e evitar o envio acidental de artefatos locais para o repositório.

### O que é ignorado

- ambiente virtual Python
- diretórios de cache e compilação
- banco SQLite local
- arquivos `.env` e variáveis de ambiente
- `local_settings.py`
- certificados, chaves e arquivos secretos
- arquivos de editor e sistema

### Boas práticas aplicadas

- não versionar `SECRET_KEY` diretamente em arquivos de configuração públicos
- não commit de arquivos locais de desenvolvimento
- manter `db.sqlite3` fora do controle de versionamento em ambientes de desenvolvimento
- usar variáveis de ambiente para segredos em produção

### Recomendação para produção

Utilize um arquivo `.env` com as variáveis necessárias e mantenha o acesso controlado por ambiente e permissões de repositório.

## Como Executar Localmente

### 1. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\portfolio-ds\Scripts\Activate.ps1
```

### 2. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 3. Rodar o servidor

```powershell
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Observações de Desenvolvimento

- O projeto está em fase de refinamento visual e navegação.
- A base de SEO já está pronta para ser expandida com Schema.org e outras marcções estruturadas.
- O menu mobile já está funcionando com comportamento responsivo em telas menores.

## Próximos Melhoramentos Sugeridos

- adicionar schema.org nas páginas principais
- aplicar imagens reais do perfil/projetos em alta qualidade
- incluir botão de download de currículo
- melhorar a seção de projetos com cards interativos e filtros
- adicionar analytics no front-end e eventos de interação

## Status Atual

### Implementado
- layout inicial da home
- navbar fixa e responsiva
- hero section tecnológica
- botões de ação centralizados
- navegação mobile com hambúrguer
- SEO básico para redes sociais e Google
- favicon e arquivos de rastreio
- proteção de artefatos sensíveis com `.gitignore`

### Em Planejamento
- refinamento final da identidade visual
- otimização para performance
- documentação adicional de deploy
- ajustes de acessibilidade e UX
- separação de configurações sensíveis por ambiente

## Licença

Este projeto está licenciado sob a licença MIT.

Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor

Danilo Silva dos Santos
