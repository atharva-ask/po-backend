from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_database_conn
from pydantic import BaseModel

app = FastAPI()
conn = get_database_conn()
cur = conn.cursor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This will allow all origins, you can specify your frontend URL instead
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class customer_query(BaseModel):
    year_val: int
    sem_val: int
    po_val: float
    sub_code: str
    po_id: str

colname =(
    'po1', 'po2', 'po3', 'po4', 'po5', 'po6', 
    'po7', 'po8', 'po9', 'po10', 'po11','po12', 
    'pso1', 'pso2', 'pso3'
    )

def getCourseNameIdmap(yearval:int, semval:int):
    cur.execute(f"""
            SELECT c_code, title FROM course 
            WHERE year = '{yearval}' AND sem = '{semval}';
        """)
    data = cur.fetchall()

    data_dict = dict()
    for row in data:
        temp = {}
        temp[row[0]] = row[1]
        data_dict.append(temp)
    return data_dict


@app.get('/subjects')
def subjects(yearval:int, semval:int):
    cur.execute(f"""
        SELECT c_code, title, id FROM course 
        WHERE year = '{yearval}' AND sem = '{semval}';
    """)

    data = cur.fetchall()
    if(len(data) == 0):
        return HTTPException(status_code=400, detail="Not sufficient data")
    
    data_list = list()
    for row in data:
        temp = {}
        temp["course_code"] = row[0]
        temp["course_name"] = row[1]
        temp["course_id"] = row[2]
        data_list.append(temp)
        
    return data_list


@app.get('/getOldPOval')
def getoldpoval(pk:int):
    # sub_char = sub.toCharArray()
    sub = ()
    res = list()
    cur.execute(f"""
        Select po1, po2, po3, po4, 
        po5, po6,po7, po8, po9,po10, 
        po11, po12 from course 
        where id = {pk}
    """)
    data = cur.fetchall()
    if(len(data) == 0):
        return HTTPException(status_code=400, detail="Not sufficient data")
    # print(data)
    res.append(data)
    cur.execute(f"""
        Select pso1, pso2, pso3
        from course 
        where id = {pk}
    """)
    data = cur.fetchall()
    if(len(data) == 0):
        return HTTPException(status_code=400, detail="Not sufficient data")
    res.append(data)

    cur.execute(f"""
        Select co_att 
        from course 
        where id = {pk}
    """)
    data = cur.fetchall()
    if(len(data) == 0):
        return HTTPException(status_code=400, detail="Not sufficient data")
    res.append(data)
    return res;



@app.put('/update_po/')
def update_po(pk: int, val: float, colname: str):

    try:
        query = f"""
            UPDATE course 
            SET {colname} = %s WHERE id = %s;
        """
        cur.execute(query, (val, pk))
        conn.commit()
        return {'message': f"Successfully updated value of {colname} to {val} of course id = {pk}"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
   

@app.get('/getIndirectPO/{year}')
def getPOIndirect(year:int):
    cur.execute(f"""
        Select * from po_indirect
        where year = {year}
    """)
    data = cur.fetchall()
    print(data)
    if(len(data) == 0):
        return HTTPException(status_code=400, detail="Not sufficient data")
    
    return data[0][0:15]


@app.post('/setIndirectPO')
def getPOIndirect(colname:str, colval:float, yearval:int):
    try :
        cur.execute(f"""
        UPDATE po_indirect
        set {colname} = {colval}
        where year = {yearval}
        """)
        conn.commit()
        return {'message': f"Successfully updated for entry of {colname} of acc year {yearval}."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get('/getTargetPO/{year}')
def getTargetPO(year: int):
    cur.execute(f"""
        select * from target_po
        where year = {year};
    """)
    data = cur.fetchall()
    # print(data)
    if(len(data) == 0):
        return HTTPException(status_code=400, detail="Not sufficient data")
    #year is sliced
    res = data[0][1:]
    return res

@app.post('/setTargetPO')
def setTargetPO(colname:str, colval:float, yearval:int):
    try :
        cur.execute(f"""
        UPDATE target_po
        set {colname} = {colval}
        where year = {yearval}
        """)
        conn.commit()
        return {'message': f"Successfully updated for entry of {colname} of acc year {yearval}."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

#Get the Direct po value of single PO
#we have to calculate for each po1-po12, Pso1-Pso3
# @app.get('/column_operation/')

def getcolumnop(colname:str):
    cur.execute(f"""
        Select {colname}, co_att from course
    """)
    data = cur.fetchall()
    # print(data)
    if(len(data) == 0):
        return HTTPException(status_code=400, detail="Not sufficient data")
    
    valnum = 0.00
    valdenom = 0.00
    temp = 0.00
    res = 0.00

    # check for null values in database
    for row in data:
        if row[0] is not None and row[1] is not None:
            temp = (row[0]) * (row[1])
            valnum += temp
            valdenom += row[0]
    
    if valdenom == 0.00:
        valdenom = 1
    res = (valnum)/(valdenom)
    return res


@app.get('/getDirectPO')
def getDirectPO(year:str):
    try:
        data_list = list()
        for name in colname:
            val = getcolumnop(name)
            data_list.append(val)
            cur.execute("""
                UPDATE po_direct 
                SET {} = %s
                WHERE year = %s
            """.format(name), (val, year))
        conn.commit()
        return data_list
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
@app.get('/getPOAttainment')
def getPOAttainment(year:int):
    list1 = list() #contains direct PO
    for name in colname:
        val = getcolumnop(name)
        list1.append(val)

    cur.execute(f"""
        Select * from po_indirect
        where year = {year}
    """)
    data = cur.fetchall()
    print(data)
    if(len(data) == 0):
        return HTTPException(status_code=400, detail="Not sufficient data")
    
    list2 = data[0]
    
    result = [0.8*x + 0.2*y for x, y in zip(list1, list2)]
    return result
    # return 1

@app.get('/ScaledPoAttainment')
def scaledPOAttainment(year : int):
    res = getPOAttainment(2023)
    result = [3*x for x in res]
    return result


@app.get('/acheivedPoAttainment')
def getacheivedPoAttainment(year : int):
    scaledPO = scaledPOAttainment(year)
    targetPO = getTargetPO(year)
    if(len(targetPO) == 0):
        return HTTPException(status_code=400, detail="Not sufficient data")

    res = [(x/y)*3 for x, y in zip(scaledPO, targetPO)]
    return res





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



