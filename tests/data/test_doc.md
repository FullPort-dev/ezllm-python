# Document
#### EzLLM Document
# a Document represents a single file uploaded to EzLLM

​
# Fundamental Concepts
​
# Document Parsing
depending on the selected parser, documents are typically parsed into markdown. There’s a few good reasons for translating a document to markdown

Preserves Essential Formatting: Converting documents to Markdown retains crucial formatting, such as tables, headers, and other layout elements, which are key to maintaining the document’s original presentation and readability.

Efficient Token Usage: Markdown uses fewer tokens to represent document formatting. Reducing the number of tokens increases speed, available context and reduces cost.

Ubiquity: Markdown is very common and as such LLMs are able to understand the content easily