{{< alert title="IMPORTANT" color="info" >}}
**The Vision Service is becoming more modular.**

By the beginning of May, the following **breaking changes** will take effect:

- You will need to create an individual vision service instance for each detector, classifier, and segementer model.
  You will no longer be able to create one vision service and register all of your detectors, classifiers, and segmenters within it.
  You will need to update your robot config and your Vision Service API calls.
- You must add and remove models using the [robot config](/manage/configuration/).
  You will no longer be able to add or remove models using the SDKs.
- The way to add machine learning vision models is changing.
  You will need to first register the machine learning model file with the [ML Model Service](/services/ml/) and then add that registered model to a vision service.

For more information, see [the Release Notes](/appendix/release-notes/#2-may-2023).

{{< /alert >}}
