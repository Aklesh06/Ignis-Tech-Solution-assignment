import JobContainer from "./JobContainer";

const JobList = ({ jobs }) => (
  <div className="job-list">
    {jobs.length > 0 ? (
      jobs.map((job) => <JobContainer key={job.id} job={job} />)
    ) : (
      <p>No jobs found.</p>
    )}
  </div>
);

export default JobList;