// Sample data received from the backend
const dataSummary = [{'column': 'Timestamp',
   'properties': {'dtype': 'date',
    'min': '2014-08-27 11:29:31',
    'max': '2014-08-27 11:32:39',
    'samples': ['2014-08-27 11:32:05',
     '2014-08-27 11:29:37',
     '2014-08-27 11:31:22'],
    'num_unique_values': 9,
    'semantic_type': '',
    'description': ''}},
  {'column': 'Age',
   'properties': {'dtype': 'number',
    'std': 4,
    'min': 31,
    'max': 44,
    'samples': [44, 35, 37],
    'num_unique_values': 8,
    'semantic_type': '',
    'description': ''}},
  {'column': 'Gender',
   'properties': {'dtype': 'category',
    'samples': ['Female', 'M', 'Male'],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'Country',
   'properties': {'dtype': 'category',
    'samples': ['United States', 'Canada', 'United Kingdom'],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'state',
   'properties': {'dtype': 'string',
    'samples': ['IN', 'MI', 'TX'],
    'num_unique_values': 5,
    'semantic_type': '',
    'description': ''}},
  {'column': 'family_history',
   'properties': {'dtype': 'category',
    'samples': ['Yes', 'No'],
    'num_unique_values': 2,
    'semantic_type': '',
    'description': ''}},
  {'column': 'treatment',
   'properties': {'dtype': 'category',
    'samples': ['No', 'Yes'],
    'num_unique_values': 2,
    'semantic_type': '',
    'description': ''}},
  {'column': 'work_interfere',
   'properties': {'dtype': 'category',
    'samples': ['Rarely', 'Sometimes'],
    'num_unique_values': 4,
    'semantic_type': '',
    'description': ''}},
  {'column': 'no_employees',
   'properties': {'dtype': 'string',
    'samples': ['More than 1000', '1-5'],
    'num_unique_values': 5,
    'semantic_type': '',
    'description': ''}},
  {'column': 'remote_work',
   'properties': {'dtype': 'category',
    'samples': ['Yes', 'No'],
    'num_unique_values': 2,
    'semantic_type': '',
    'description': ''}},
  {'column': 'tech_company',
   'properties': {'dtype': 'category',
    'samples': ['No', 'Yes'],
    'num_unique_values': 2,
    'semantic_type': '',
    'description': ''}},
  {'column': 'benefits',
   'properties': {'dtype': 'category',
    'samples': ['Yes', "Don't know"],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'care_options',
   'properties': {'dtype': 'category',
    'samples': ['Not sure', 'No'],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'wellness_program',
   'properties': {'dtype': 'category',
    'samples': ["Don't know", 'No'],
    'num_unique_values': 2,
    'semantic_type': '',
    'description': ''}},
  {'column': 'seek_help',
   'properties': {'dtype': 'category',
    'samples': ['Yes', "Don't know"],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'anonymity',
   'properties': {'dtype': 'category',
    'samples': ['Yes', "Don't know"],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'leave',
   'properties': {'dtype': 'category',
    'samples': ["Don't know", 'Very difficult'],
    'num_unique_values': 4,
    'semantic_type': '',
    'description': ''}},
  {'column': 'mental_health_consequence',
   'properties': {'dtype': 'category',
    'samples': ['No', 'Maybe'],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'phys_health_consequence',
   'properties': {'dtype': 'category',
    'samples': ['No', 'Yes'],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'coworkers',
   'properties': {'dtype': 'category',
    'samples': ['Some of them', 'No'],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'supervisor',
   'properties': {'dtype': 'category',
    'samples': ['No', 'Yes'],
    'num_unique_values': 2,
    'semantic_type': '',
    'description': ''}},
  {'column': 'mental_health_interview',
   'properties': {'dtype': 'category',
    'samples': ['No', 'Yes'],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'phys_health_interview',
   'properties': {'dtype': 'category',
    'samples': ['Maybe', 'No'],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'mental_vs_physical',
   'properties': {'dtype': 'category',
    'samples': ['Yes', "Don't know"],
    'num_unique_values': 3,
    'semantic_type': '',
    'description': ''}},
  {'column': 'obs_consequence',
   'properties': {'dtype': 'category',
    'samples': ['Yes', 'No'],
    'num_unique_values': 2,
    'semantic_type': '',
    'description': ''}}];

// Helper function to handle NaN values
function handleNaN(value) {
    return (value === "nan" || isNaN(value)) ? "N/A" : value;
}

// Function to create data summary cards inside the "summary-content" section
function displayDataSummary(data) {
    const container = document.getElementById("summary-content");

    data.forEach(item => {
        // Create the card container
        const card = document.createElement("div");
        card.classList.add("summary-card");

        // Column name as the heading
        const columnTitle = document.createElement("h3");
        columnTitle.textContent = item.column;
        card.appendChild(columnTitle);

        // Dtype
        const dtype = document.createElement("p");
        dtype.textContent = `Type: ${handleNaN(item.properties.dtype)}`;
        card.appendChild(dtype);

        // Unique, min, and max with NaN handling
        const uniqueMinMax = document.createElement("p");
        uniqueMinMax.textContent = `Unique: ${handleNaN(item.properties.num_unique_values)}, Min: ${handleNaN(item.properties.min)}, Max: ${handleNaN(item.properties.max)}`;
        card.appendChild(uniqueMinMax);

        // Expand/collapse button for samples
        const sampleButton = document.createElement("button");
        sampleButton.classList.add("sample-toggle-btn");
        sampleButton.textContent = "View Samples v";
        sampleButton.onclick = () => toggleSamples(samplesDiv, sampleButton);
        card.appendChild(sampleButton);

        // Sample values section (initially hidden)
        const samplesDiv = document.createElement("div");
        samplesDiv.classList.add("samples");
        samplesDiv.style.display = "none";
        samplesDiv.textContent = `Samples: ${item.properties.samples.length > 0 ? item.properties.samples.join(', ') : "N/A"}`;
        card.appendChild(samplesDiv);

        // Append the card to the container
        container.appendChild(card);
    });
}

// Function to toggle the display of sample values
function toggleSamples(samplesDiv, button) {
    if (samplesDiv.style.display === "none") {
        samplesDiv.style.display = "block";
        button.textContent = "Hide Samples ^";
    } else {
        samplesDiv.style.display = "none";
        button.textContent = "View Samples v";
    }
}

// Function to toggle sections (Summary, Goals) visibility
function toggleSection(sectionId, button) {
    const section = document.getElementById(sectionId);
    if (section.style.display === "none") {
        section.style.display = "block";
        button.textContent = "^";
    } else {
        section.style.display = "none";
        button.textContent = "v";
    }
}

// Call the function to display data summary cards on page load
displayDataSummary(dataSummary);
