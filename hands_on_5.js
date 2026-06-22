```javascript
use("student_information_system");

db.feedback.insertMany([
{
student_id:1,
course_code:"CS101",
semester:"2022-ODD",
rating:5,
comments:"Excellent teaching. Would recommend.",
tags:["challenging","well-structured","good-examples"],
submitted_at:new Date("2022-11-30T10:15:00Z"),
attachments:[
{filename:"notes.pdf",size_kb:240}
]
},
{
student_id:2,
course_code:"CS101",
semester:"2022-ODD",
rating:4,
comments:"Very informative.",
tags:["good-examples","interactive"],
submitted_at:new Date("2022-11-28T09:20:00Z"),
attachments:[
{filename:"lab.pdf",size_kb:180}
]
},
{
student_id:3,
course_code:"CS101",
semester:"2021-EVEN",
rating:2,
comments:"Needs more practical sessions.",
tags:["challenging","fast-paced"],
submitted_at:new Date("2021-12-01T11:30:00Z"),
attachments:[
{filename:"feedback.docx",size_kb:120}
]
},
{
student_id:4,
course_code:"CS102",
semester:"2022-ODD",
rating:5,
comments:"Database concepts explained well.",
tags:["well-structured","practical"],
submitted_at:new Date("2022-11-25T12:10:00Z"),
attachments:[
{filename:"db.pdf",size_kb:210}
]
},
{
student_id:5,
course_code:"CS102",
semester:"2021-EVEN",
rating:3,
comments:"Average course.",
tags:["moderate","assignments"],
submitted_at:new Date("2021-11-29T14:00:00Z"),
attachments:[
{filename:"assignment.pdf",size_kb:300}
]
},
{
student_id:6,
course_code:"CS103",
semester:"2022-ODD",
rating:5,
comments:"Excellent OOP examples.",
tags:["coding","good-examples"],
submitted_at:new Date("2022-11-27T10:00:00Z"),
attachments:[
{filename:"oop.pdf",size_kb:160}
]
},
{
student_id:7,
course_code:"EC101",
semester:"2022-EVEN",
rating:4,
comments:"Interesting subject.",
tags:["interactive","concepts"],
submitted_at:new Date("2023-04-15T09:30:00Z"),
attachments:[
{filename:"circuits.pdf",size_kb:270}
]
},
{
student_id:8,
course_code:"ME101",
semester:"2022-EVEN",
rating:1,
comments:"Difficult to follow.",
tags:["challenging","lengthy"],
submitted_at:new Date("2023-04-20T16:00:00Z"),
attachments:[
{filename:"thermo.pdf",size_kb:320}
]
},
{
student_id:9,
course_code:"CS103",
semester:"2022-ODD",
rating:4,
comments:"Good assignments.",
tags:["assignments","coding"],
submitted_at:new Date("2022-11-29T13:40:00Z"),
attachments:[
{filename:"project.zip",size_kb:512}
]
},
{
student_id:10,
course_code:"CS102",
semester:"2022-ODD",
rating:5,
comments:"Highly recommended.",
tags:["challenging","excellent"],
submitted_at:new Date("2022-11-26T08:45:00Z")
}
]);

db.feedback.countDocuments();







Task-2: CRUD Operations
db.student_feedback.countDocuments();

db.student_feedback.find({
    rating: 5
});

db.student_feedback.find({
    course_code: "CS101"
});

db.student_feedback.updateOne(
    {
        student_id: 5
    },
    {
        $set: {
            rating: 4
        }
    }
);

db.student_feedback.updateOne(
    {
        student_id: 3
    },
    {
        $push: {
            tags: "needs-improvement"
        }
    }
);

db.student_feedback.deleteOne({
    student_id: 8
});

db.student_feedback.find().pretty();





Task-3: Aggregation Pipeline
db.student_feedback.aggregate([
{
    $group: {
        _id: "$course_code",
        average_rating: {
            $avg: "$rating"
        },
        total_feedback: {
            $sum: 1
        }
    }
}
]);

db.student_feedback.aggregate([
{
    $group: {
        _id: "$semester",
        feedback_count: {
            $sum: 1
        }
    }
}
]);

db.student_feedback.aggregate([
{
    $unwind: "$tags"
},
{
    $group: {
        _id: "$tags",
        frequency: {
            $sum: 1
        }
    }
},
{
    $sort: {
        frequency: -1
    }
}
]);

db.student_feedback.createIndex({
    course_code: 1
});

db.student_feedback.getIndexes();

db.student_feedback.createIndex({ course_code: 1 });

db.student_feedback.find({
    course_code: "CS101"
}).explain("executionStats");
```
