import PipelineStep from './PipelineStep';
import usePipeline from '../../hooks/usePipeline';
import PlusIcon from '../../components/icons/PlusIcon';

const Pipeline = () => {
  const { pipeline, handleAddStep } = usePipeline();

  return (
    <main id="pipline_page">
      {pipeline.map((pipeline) => (
        <PipelineStep pipeline={pipeline} key={pipeline.id} />
      ))}

      <div onClick={handleAddStep} id="add_step">
        <PlusIcon />
      </div>
    </main>
  );
};

export default Pipeline;
