import PipelineStep from './PipelineStep';
import usePipeline from '../../hooks/usePipeline';

const Pipeline = () => {
  const { pipeline, handleAddStep } = usePipeline();

  return (
    <main>
      {pipeline.map((pipeline, index) => (
        <PipelineStep pipeline={pipeline} key={index} />
      ))}

      <button onClick={handleAddStep}>+</button>
    </main>
  );
};

export default Pipeline;
