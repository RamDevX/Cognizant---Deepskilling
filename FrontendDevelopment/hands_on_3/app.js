import { courses } from "./data.js";

const courseGrid = document.querySelector(".course-grid");
const totalCredits = document.getElementById("total-credits");
const selectedCourse = document.getElementById("selected-course");
const searchInput = document.getElementById("search-courses");
const sortButton = document.getElementById("sort-btn");

let courseList = [...courses];

function displayCourses(courseArray) {

    courseGrid.innerHTML = "";

    courseArray.forEach(course => {

        const card = document.createElement("div");
        card.className = "course-card";

        card.innerHTML = `
            <h3>${course.name}</h3>
            <p><strong>Code:</strong> ${course.code}</p>
            <p><strong>Credits:</strong> ${course.credits}</p>
            <p><strong>Grade:</strong> ${course.grade}</p>
            <button>View Details</button>
        `;

        const button = card.querySelector("button");

        button.addEventListener("click", () => {

            selectedCourse.innerHTML = `
                Selected Course:
                <strong>${course.name}</strong>
                (${course.code})
            `;

        });

        courseGrid.appendChild(card);

    });

}

displayCourses(courseList);

const total = courseList.reduce((sum, course) => sum + course.credits, 0);

totalCredits.textContent = `Total Credits : ${total}`;

searchInput.addEventListener("keyup", () => {

    const keyword = searchInput.value.toLowerCase();

    const filtered = courseList.filter(course =>
        course.name.toLowerCase().includes(keyword)
    );

    displayCourses(filtered);

});

sortButton.addEventListener("click", () => {

    courseList.sort((a, b) => a.credits - b.credits);

    displayCourses(courseList);

});

console.log("Original Courses");
console.table(courses);

console.log(
    courses.map(course => course.name)
);

console.log(
    courses.filter(course => course.credits >= 4)
);

console.log(
    courses.reduce((sum, c) => sum + c.credits, 0)
);