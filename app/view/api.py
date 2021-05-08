""" ---- Communications ---- """
# Signals to connect with control API
ui_signals = {}
# Widgets to be updated by view API
ui_updates = {}

def add_to_signal_map(signal, signal_key):
  if signal_key in ui_signals.keys():
      raise ValueError(f"Signal Key already exists with the value {repr(ui_signals[signal_key])}." 
                        + "Please assign widget with alternative signal key.")
  else:
    ui_signals[signal_key] = signal

def add_to_update_map(widget_func, update_key):
  if update_key in ui_updates.keys():
    raise ValueError(f"Update Key already exists with the value {repr(ui_updates[update_key])}." 
                    + "Please assign widget with alternative update key.")
  else:
    ui_updates[update_key] = widget_func

""" ----------- View Setup ----------- """
""" Add Model-Specific Choices/Information. """
def addTrainingPipelines():
  pass
# Combobox Choice, Description, and default hyperparameters
# Followed by refreshInferenceWeights()


""" ---- View API: Model Panel ---- """
def displayProgressPresentation(update_string):
  ui_updates['update_train_feedback'](update_string)

def displayTrainingErrorPresentation(error_string):
  ui_updates['update_train_feedback'](error_string)

def disableTrainButton():
  ui_updates['update_train_button']['disable']()

def enableTrainButton():
  ui_updates['update_train_button']['enable']()

""" ---- View API: Inference Panel ---- """
def refreshInferenceWeightFeedback(feedback_string):
  ui_updates['update_weight_panel_feedback'](feedback_string)

def displayInferenceErrorPresentation(error_string):
  ui_updates['update_inference_feedback'](error_string)

""" ---- View API: Inference Explorer ---- """
def presentInferenceView(image_path, label, slider_max):
  ui_updates['launch_inference_dialog'](image_path, label, slider_max)
  
def updateInferenceView(image_path, label):
  ui_updates['toggle_inference'](image_path, label)

def updateSliderLength(length):
  ui_updates['update_slider_length'](length)

  """ ---- View API: Database View ---- """
def refreshDatabaseWeights(pipeline, weight_names):
  ui_updates['update_weight_list'](pipeline, weight_names)