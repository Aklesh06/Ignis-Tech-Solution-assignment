import { useState,useEffect } from "react";
import axios from "axios";
import SearchBar from "./components/SearchBar";
import JobList from "./components/JobList";
import "./App.css";

function App() {

  const [jobs, setJobs] = useState([]);
  const [allJobs, setAllJobs] = useState([]);

  useEffect(() => {

    axios.get('http://127.0.0.1:8000/api/jobs/') 
      .then(response => {; 
        setJobs(response.data.jobs);
        setAllJobs(response.data.jobs);  
      })
      .catch(error => {
        console.error('There was an error fetching the job data!', error);
      });
  }, []); 

  const handleSearch = (searchTerm) => {
    const filteredJobs = allJobs.filter(
      (job) =>
        job.job_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.employee_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.location_type.some((loc_type) =>
          loc_type.toLowerCase().includes(searchTerm.toLowerCase()) 
        )
        ||
        job.skills.some((skill) =>
          skill.toLowerCase().includes(searchTerm.toLowerCase())
        )
    );
    console.log(filteredJobs)
    setJobs(filteredJobs);
  };

  return (
    <div className="App">
      <SearchBar onSearch={handleSearch} />
      <JobList jobs={jobs} />
    </div>
  );
}

export default App;