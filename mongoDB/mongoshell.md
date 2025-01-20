# mongoDB 자주 사용하는 shell script


1. 해당 콜렉션에서 모든 필드의 데이터 타입 출력 
```
db.collection_name.aggregate([
  { 
    $project: { 
      fields: { $objectToArray: "$$ROOT" } // 문서를 key-value 배열로 변환
    }
  },
  { $unwind: "$fields" // 배열을 개별 요소로 펼침 
  },
  { 
    $group: { 
      _id: "$fields.k", // 필드 이름별로 그룹화
      types: { $addToSet: { $type: "$fields.v" } } // 필드의 타입을 집합으로 저장
    }
  }
]).forEach(printjson)

```

2. 해당 콜렉션에서 특정 필드의 타입 확인 
db.collection_name.aggregate([
  { $project: { fieldType: { $type: "$출생년도" } } }
])