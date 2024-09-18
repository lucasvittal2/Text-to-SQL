# Text To SQL API 👨‍💻📈🛢️

## Introduction
This project is a personal initiative of  constructing  contructing an Text-to-SQL Restful API. The main idea of this application is generate a SQL query with a natural question so that non-technical users can make some consulting on database without knowing anything about
about SQL or database schema. The base of working of this application is a proper metadata and it envolves a lot of challenges:

  - Set properly a set of metadata about database schema
  - The database schema should have coherent schema with table names , columns names and relationships between tables properly set
  - The joins revealed to be a big problema, so the database schema should be in a format that avoids the using of joins in the query.

Even through This application brings big challenges it has High pespective of integration with chatbots and visualizations tools,so on near future we are pretending  to implementing some integration, so we're gonna embrace this challenges and revolutionazing the future of data analysis

## Application Diagram 👨🏾‍🔧🔧
For the development of the application we used docker container holding stacks like: 

  - ChromaDB for vector storing and semanthic search;
  - Python and FastAPI for implementing a Restful API
  - PostgresSQL interfaced with main container (text_to_sql_api) by adminer
    
![App Diagram](https://github.com/user-attachments/assets/e1cf4b9e-dac5-41ba-a165-f70ed37962f6)

## Logic Flux 👷🪛

![Logic Flux](https://github.com/user-attachments/assets/b7edef47-3b10-467a-a2b8-5c283fbf0bea)



## 🎯 Objectives

- Making non-technical users being able to make consulting in database
- making an scalable api able to attend diverse users.
-  Integrate this tool with visualization tools.
      


## ✅ Result

This solution allowed the conversion of natural query into a sql query using GPT-4o and OpenAI embeddings:

![image](https://github.com/user-attachments/assets/f23a74e4-2931-4c03-bdce-531bd16c85a4)



## 🚀 How to Set Up and Run the project

Follow these steps 📝 to clone, set up, and run the Text-to-SQL API

### Step-by-Step Instructions 📋

1. **Clone the Project** 🌀

   ```bash
   $> git clone https://github.com/lucasvittal2/Text-to-SQL.git
   ```

2. **Navigate to the Project Folder** 📁

   ```bash
   $> cd <FOLDER_YOU_CLONED>/Text-to-SQL
   ```

3. **create docker network 'devnet'** 🛠️

   ```bash
   $> docker network create --subnet 172.10.0.0/16 devnet
   ```

4. **build containers using docker-compose** 🐋

   ```bash
   $> docker-compose up --build -d
   ```

7. **Ready to Test and Improve** 🚀

   Now you are ready to test and even improve my solution. 😎✊✨

   you can consume the API through [http://localhost:8090/](http://localhost:8090/docs#)

   through end points:

   [POST] - /text-to-sql/generateSQL
     body:
         question: <str>
         
   [GET] - /items/UpdateMetadataEmbeddings
       Note: If you want update database schema or using a diferrent schema, consider make modification on files ./assets/json/tables.jsonl and ./assets/json/columns.jsonl mataining the same keys and changing the values or adding new lines.



