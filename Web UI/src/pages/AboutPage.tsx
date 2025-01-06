const AboutPage = () => {
  return (
    <main id="about_us_page">
      <h2>About us</h2>
      <p>
        We are a group of students from the Kyiv Polytechnic Institute: Oleksandr, Maksym, Nazar, and Mykhailo, from group TV-22. This website is a project developed as part of our coursework. It serves as a demonstration of our efforts in building a functional tool for audio analysis.
      </p>
      <br/>
      <p>
        Our platform allows users to upload audio files in the .wav format. If the audio contains multiple channels, you have the option to separate them for individual processing. Additionally, the site supports an unlimited number of audio signal processing actions, organized in a pipeline structure. Each step in the pipeline processes the modified file from the previous step, ensuring a streamlined workflow. The final result of the pipeline is provided as a downloadable .zip archive.
      </p>
      <br/>
      <p>
        We hope you find this tool helpful for exploring audio processing capabilities!
      </p>
    </main>
  );
};

export default AboutPage;
