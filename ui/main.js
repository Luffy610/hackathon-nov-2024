// Simulated backend data (can be dynamic from an API)
function renderDataSummary(data) {
     const dataGrid = document.querySelector('#data-grid');
     dataGrid.innerHTML = '';  // Clear previous content

     data.forEach(item => {
         const container = document.createElement('div');
         container.classList.add('data-container');

         // Column Name (e.g., TransactionID)
         const columnTitle = document.createElement('h3');
         columnTitle.textContent = item.column;  // Show the column name (e.g., TransactionID)
         container.appendChild(columnTitle);

         // Properties Section (e.g., dtype, semantic_type, description)
         const propertiesContainer = document.createElement('div');
         propertiesContainer.classList.add('properties-container');

         // Data Type
         const dtype = document.createElement('p');
         dtype.innerHTML = `<strong>Data Type:</strong> ${item.properties.dtype}`;
         propertiesContainer.appendChild(dtype);

         // Semantic Type
         const semanticType = document.createElement('p');
         semanticType.innerHTML = `<strong>Semantic Type:</strong> ${item.properties.semantic_type}`;
         propertiesContainer.appendChild(semanticType);

         // Description
         const description = document.createElement('p');
         description.innerHTML = `<strong>Description:</strong> ${item.properties.description}`;
         propertiesContainer.appendChild(description);

         // Number of Unique Values
         const numUnique = document.createElement('p');
         numUnique.innerHTML = `<strong>Unique Values:</strong> ${item.properties.num_unique_values}`;
         propertiesContainer.appendChild(numUnique);

         // Sample Values
         const sampleValues = document.createElement('p');
         sampleValues.innerHTML = `<strong>Sample Values:</strong> ${item.properties.samples.join(', ')}`;
         propertiesContainer.appendChild(sampleValues);

         container.appendChild(propertiesContainer);

         // Append the container to the grid
         dataGrid.appendChild(container);
     });
 }

// Function to render goals dynamically
function renderGoals(goals) {
    const goalsContainer = document.querySelector('#goals-container');
    goalsContainer.innerHTML = '';  // Clear previous content

    goals.forEach(goal => {
        const goalContainer = document.createElement('div');
        goalContainer.classList.add('goal-container');

        // Question Section
        const questionTitle = document.createElement('h4');
        questionTitle.textContent = goal.question;  // Display the goal question
        goalContainer.appendChild(questionTitle);

        // Visualization Section
        const visualization = document.createElement('p');
        visualization.innerHTML = `<strong>Suggested Visualization:</strong> ${goal.visualization}`;
        goalContainer.appendChild(visualization);

        // Rationale Section
        const rationale = document.createElement('p');
        rationale.innerHTML = `<strong>Rationale:</strong> ${goal.rationale}`;
        goalContainer.appendChild(rationale);

        // Append the goal container to the goals container
        goalsContainer.appendChild(goalContainer);

        goalContainer.addEventListener('click', () => {
            handleGoalClick(goal, goalContainer)
        });

        if (goal.index === 0) {
            goalContainer.classList.add('selected');  // Highlight the first goal container
        }
    });
}

function renderChart(bytes){
    const chartImage = new Image();
    chartImage.src = bytes;
    const chartImageContainer = document.getElementById('chart-image-container');
    chartImageContainer.innerHTML = '';  // Clear previous content
    chartImageContainer.appendChild(chartImage);
}

function renderCode(code){
    const chartCodeContainer = document.getElementById('chart-code');
    const cleanedCode = code.replace(/^```/gm, '').replace(/```$/gm, '').trim();
    chartCodeContainer.textContent = cleanedCode;
    }

 // Fetch data from the backend (e.g., via an API)
 async function fetchData() {
     try {
         const response = await fetch('http://localhost:8080/defaultchart/');
         const data = await response.json();
         renderDataSummary(data.summary.fields);  // Pass the JSON data to render function
         renderGoals(data.goals);
         renderChart(data.chart_response)
         renderCode(data.chart_code)
     } catch (error) {
         console.error('Error fetching data:', error);
     }
 }

 // Call fetchData when the page loads
 window.onload = fetchData;



// Function to toggle Data Summary section visibility
function toggleDataSummary() {
    const dataGrid = document.getElementById('data-grid');
    const collapseBtn = document.getElementById('collapse-data-btn');

    // If the section is expanded, collapse it
    if (dataGrid.style.maxHeight !== '0px') {
        // Collapse the section
        dataGrid.style.maxHeight = '0';  // Collapse to 0px height
        dataGrid.style.visibility = 'hidden';  // Hide the content
        collapseBtn.innerText = 'Expand Data Summary';  // Change button text
    } else {
        // Expand the section
        dataGrid.style.maxHeight = dataGrid.scrollHeight + "px";  // Expand to full content height
        dataGrid.style.visibility = 'visible';  // Make the content visible
        collapseBtn.innerText = 'Collapse Data Summary';  // Change button text
    }
}

// Function to toggle Data Summary section visibility
function toggleGoalSelection() {
    const goalsContainer = document.getElementById('goals-container');
    const collapseBtn = document.getElementById('collapse-goals-btn');

    // If the section is expanded, collapse it
    if (goalsContainer.style.maxHeight !== '0px') {
        // Collapse the section
        goalsContainer.style.maxHeight = '0';  // Collapse to 0px height
        goalsContainer.style.visibility = 'hidden';  // Hide the content
        collapseBtn.innerText = 'Expand Goals';  // Change button text
    } else {
        // Expand the section
        goalsContainer.style.maxHeight = goalsContainer.scrollHeight + "px";  // Expand to full content height
        goalsContainer.style.visibility = 'visible';  // Make the content visible
        collapseBtn.innerText = 'Collapse Goals';  // Change button text
    }
}

// Ensure the section is expanded by default when the page is loaded
document.addEventListener("DOMContentLoaded", function() {
const dataGrid = document.getElementById('data-grid');
const collapseDataBtn = document.getElementById('collapse-data-btn');
const goalsContainer = document.getElementById('goals-container');
const collapseGoalsBtn = document.getElementById('collapse-goals-btn');

    // On page load, expand the section by default
    dataGrid.style.maxHeight = "900px";  // Set height to scrollHeight to expand fully
    dataGrid.style.visibility = 'visible';  // Ensure the section is visible
    collapseDataBtn.innerText = 'Collapse Data Summary';  // Set button text to "Collapse"
    const size = goalsContainer.getBoundingClientRect()
    console.log(size)
    goalsContainer.style.maxHeight = "1000px";  // Expand to full content height
    goalsContainer.style.visibility = 'visible';  // Make the content visible
    collapseGoalsBtn.innerText = 'Collapse Goals';  // Change button text
});


function copyCode() {
    const chartCodeContainer = document.getElementById('chart-code');

    // Create a temporary text area to select and copy the content
    const textarea = document.createElement('textarea');
    textarea.value = chartCodeContainer.textContent; // Includes the cleaned code (without backticks)
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
}

async function generateChart() {
    const promptInput = document.getElementById('prompt-input').value.trim();

    // Check if prompt is empty
    if (!promptInput) {
        alert('Please enter a prompt to generate the chart.');
        return;
    }

    try {
        // Send the prompt to the backend as a query parameter in the GET request
        const response = await fetch(`http://localhost:8080/generatechart/?goal=${encodeURIComponent(promptInput)}`);
        const data = await response.json();

        // Log the new data to check the response
        console.log('Updated Chart Data:', data);

        // If base64Image is returned, create an image element and append it
        const chartImageContainer = document.getElementById('chart-image-container');
        chartImageContainer.innerHTML = '';  // Clear previous content

        const chartImage = new Image();
        chartImage.src = data.chart_response;
        chartImageContainer.appendChild(chartImage);

        // If chartCode is returned, insert it into the 'chart-code' pre element
        const chartCodeContainer = document.getElementById('chart-code');
        let code = data.chart_code
        const cleanedCode = code.replace(/^```/gm, '').replace(/```$/gm, '').trim();
        chartCodeContainer.textContent = cleanedCode;


    } catch (error) {
        console.error('Error generating chart:', error);
    }
}

async function handleGoalClick(goal, goalContainer){

    const previouslySelected = document.querySelector('.goal-container.selected');
    if (previouslySelected) {
        previouslySelected.classList.remove('selected');
    }

        // Add 'selected' class to the clicked container
    goalContainer.classList.add('selected');
    console.log(goal)
    try {
         // Send the prompt to the backend as a query parameter in the GET request
         let response = await fetch(`http://localhost:8080/generatechart/?goal=${goal.question}`);
         console.log(response)
         let data =  await response.json();

         // Log the new data to check the response
         console.log('Updated Chart Data:', data);

         // If base64Image is returned, create an image element and append it
         const chartImageContainer = document.getElementById('chart-image-container');
         chartImageContainer.innerHTML = '';  // Clear previous content

         const chartImage = new Image();
         chartImage.src = data.chart_response;
         chartImageContainer.appendChild(chartImage);

         // If chartCode is returned, insert it into the 'chart-code' pre element
         const chartCodeContainer = document.getElementById('chart-code');
         let code = data.chart_code
         const cleanedCode = code.replace(/^```/gm, '').replace(/```$/gm, '').trim();
         chartCodeContainer.textContent = cleanedCode;


         }
         catch (error)
         {
             console.error('Error generating chart:', error);
         }}


async function handleContentRequest(type) {
    // Define the container for the new content (explanation, repair, or refinement)
    const additionalContent = document.getElementById('additional-content');
    const explanationContent = document.getElementById('explanation-content');
    const repairContent = document.getElementById('repair-content');
    const refinementContent = document.getElementById('refinement-content');

    // Clear previous content
    explanationContent.innerHTML = '';
    repairContent.innerHTML = '';
    refinementContent.innerHTML = '';

    // Show the additional content container
    additionalContent.style.display = 'block';

    // Send the GET request to the backend
    try {
        // Make the GET request to the backend based on the selected type
        const chartCodeContainer = document.getElementById('chart-code');
        const code = chartCodeContainer.innerText
        console.log(code)
        if (code){
        let response = await fetch(`http://localhost:8080/explain/?code=${encodeURIComponent(code)}`);
        console.log(response)
        let data =  await response.json();

        // Log the response to ensure we're getting the correct data
        // Update the respective section based on the type
        if (type === 'explain') {
            let htmlContent = '<h3>Data Summary:</h3>';
                htmlContent += `
                    <div class="data-container">
                        <p>${data}</p>
                    </div>
                `;
            explanationContent.innerHTML = htmlContent;
            explanationContent.classList.add('visible');
        }
        }

    } catch (error) {
        console.error('Error fetching content:', error);
    }
}

// Add event listeners to buttons
document.getElementById('explain-btn').addEventListener('click', () => handleContentRequest('explain'));
document.getElementById('repair-btn').addEventListener('click', () => handleContentRequest('repair'));
document.getElementById('refine-btn').addEventListener('click', () => handleContentRequest('refine'));