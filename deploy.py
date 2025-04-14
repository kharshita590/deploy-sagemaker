from sagemaker.pytorch.model import PyTorchModel

model = PyTorchModel(
    model_data="s3-model-uri",  
    role="role-iam",
    framework_version='2.5',
    py_version='py311',
    entry_point='serve.py',
    source_dir='new',
    env={
         "SAGEMAKER_REQUIREMENTS": "requirements.txt",
         
    }
)
predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium',
    endpoint_name="kippss-tts"
)

print(predictor)
print(model)
