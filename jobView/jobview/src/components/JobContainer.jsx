import React, { useEffect, useState } from "react";

const JobContainer = ({ job }) => {
  const [postTimeDiff, setPostTimeDiff] = useState("");
  const [updateTimeDiff, setUpdateTimeDiff] = useState("");

  useEffect(() => {
    const post_targetDate = new Date(job.posted_at);
    const update_targetDate = new Date(job.posted_at);
    const currentDate = new Date();

    const postDiffInMs = currentDate - post_targetDate;
    const uploadDiffInMs = currentDate - update_targetDate;

    const postDiffInSeconds = Math.floor(postDiffInMs / 1000);
    const updateDiffInSeconds = Math.floor(uploadDiffInMs / 1000);
    const postDiffInMinutes = Math.floor(postDiffInSeconds / 60);
    const updateDiffInMinutes = Math.floor(updateDiffInSeconds / 60);
    const postDiffInHours = Math.floor(postDiffInMinutes / 60);
    const updateDiffInHours = Math.floor(updateDiffInMinutes / 60);
    const postDiffInDays = Math.floor(postDiffInHours / 24);
    const updateDiffInDays = Math.floor(updateDiffInHours / 24);

    const postDays = postDiffInDays;
    const updateDays = updateDiffInDays;
    const postHours = postDiffInHours % 24;
    const updateHours = updateDiffInHours % 24;
    const postMinutes = postDiffInMinutes % 60;
    const updateMinutes = updateDiffInMinutes % 60;
    const postSeconds = postDiffInSeconds % 60;
    const updateSeconds = updateDiffInSeconds % 60;

    let postTimeString = "";

    if (postDays > 0) postTimeString += `${postDays} days ago`;
    else if (postHours > 0) postTimeString += `${postHours} hours ago`;
    else if (postMinutes > 0) postTimeString += `${postMinutes} minutes ago`;
    else if (postSeconds > 0 || postTimeString === "") postTimeString += `${postSeconds} seconds ago`;

    let updateTimeString = "";

    if (updateDays > 0) updateTimeString += `${updateDays} days ago`;
    else if (updateHours > 0) updateTimeString += `${updateHours} hours ago`;
    else if (updateMinutes > 0) updateTimeString += `${updateMinutes} minutes ago`;
    else if (updateSeconds > 0 || updateTimeString === "") updateTimeString += `${updateSeconds} seconds ago`;

    setPostTimeDiff(postTimeString);
    setUpdateTimeDiff(updateTimeString);
  }, []);
      return(
        <div className="job-container">
          <div className="job-header">
            <p>posted at {postTimeDiff}</p>
            <p>
              {job.location_type.join(", ")}
            </p>
            <p>{job.location}</p>
          </div>
          <div className="job-body">
            <div className="left-section">
              <img src={job.company_logo} alt="logo" className="logo"/>
            </div>
            <div className="middle-section">
              <h3><a href={job.job_link}>{job.job_title}</a></h3>
              <p>{job.company}</p>
              <p>{postTimeDiff} | {updateTimeDiff}</p>
            </div>
            <div className="right-section">
              <p>{job.employee_type}</p>
              <p> {job.compensation}</p>
            </div>
          </div>
          <div className="job-footer">
            <p className="skills"><strong>Skills:</strong> {job.skills.join(", ")}</p>
            <p className="descrip"><strong>Description:</strong> {job.job_description}</p>
          </div>
        </div>
      );
  }
  
  export default JobContainer;
