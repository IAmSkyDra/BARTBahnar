# Apache Solr Setup Guide (Windows)

## 1. Download & Install Solr
1. Download the latest Solr version from:  
   [https://solr.apache.org/downloads.html](https://solr.apache.org/downloads.html)

2. Extract the downloaded `.zip` file to a preferred location.

3. Open **Command Prompt (cmd)** and navigate to the Solr folder:
   ```sh
   cd path\to\solr-9.x.x\bin
   ```

## 2. Start Solr
Run the following command to start Solr in standalone mode:
```sh
solr start
```
By default, Solr runs on **port 8983**.

## 3. Access Solr Admin Panel
Once Solr is running, open your browser and go to:
```
http://localhost:8983/solr
```
This is the **Solr URL** where you can manage collections and query data.

## 4. Create a Core in Solr
Before indexing data, you need to create a core. Open **Command Prompt (cmd)** and run:
```sh
solr create -c my_core
```
- Replace `my_core` with your desired core name.

After creation, you can see your core in the **Solr Admin Panel**:  
👉 [http://localhost:8983/solr](http://localhost:8983/solr)

## 5. Get Core URL for API Use
Once the core is created, you can access it using:
```
http://localhost:8983/solr/my_core
```
Replace `my_core` with your actual core name.

### Example: Query all data in the core
```
http://localhost:8983/solr/my_core/select?q=*
```

## 6. Stop Solr
To stop Solr, use:
```sh
solr stop
```

---

Now you’re ready to use Solr on Windows! 🚀
