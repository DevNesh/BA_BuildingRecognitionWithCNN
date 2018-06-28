using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FlyHandler : MonoBehaviour {

	public CameraHandler CameraHandler;

	[Header("General")]
	public float XRadiusSteps = 0;
	public float YRotationSteps = 16;
	public float ZRotationSteps = 8;

	[Header("Focus Screenshots")]
	public GameObject FocusPoint;
	public GameObject Target;

	public float minDistanceFocus = 30;
	public float maxDistanceFocus = 70;

	[Header("Scene Screenshots")]
	public GameObject ScenePoint;
	public GameObject BoundingBox;

	public float minDistanceScene = 70;
	public float maxDistanceScene = 100;

	public int CubeSteps = 1;

	private const float ZRotationAngle = 70;
	private const float YRotationAngle = 360;

	private int i = 0;


	private void Update()
	{
		if (Input.GetKeyDown("u"))
		{
			StartCoroutine(CalculateOrbitCamera(minDistanceFocus, maxDistanceFocus, TakeScreenShotToFocusPoint));
		}

		if (Input.GetKeyDown("i"))
		{
			StartCoroutine(CalculateOrbitCamera(minDistanceScene, maxDistanceScene, TakeScreenshotToAllViewPoints));
		}
	}

	public delegate IEnumerator ScreenShotMethod();

	public IEnumerator TakeScreenShotToFocusPoint()
	{
		transform.position += Target.transform.position;
		transform.position = new Vector3(transform.position.x, transform.position.y - Target.transform.position.y, transform.position.z);
		transform.LookAt(Target.transform.position);

		if (CameraHandler.IsInsideBuilding(transform.position))
		{
			yield return null;
		}
		else
		{
			i++;
			//if (i > 2873)
			//{
			//Debug.Log("Ankommer");
			//Instantiate(FocusPoint, transform.position, Quaternion.identity);
			Debug.Log(i);
			yield return StartCoroutine(CameraHandler.TakeScreenshots(i));
			//}
			//else
			//{
			//	Debug.Log(i);
			//	yield return null;
			//}
		}
	}

	private IEnumerator TakeScreenshotToAllViewPoints()
	{
		Bounds bb = BoundingBox.GetComponent<BoxCollider>().bounds;

		float witdh = bb.max.x - bb.min.x;
		float height = bb.max.y - bb.min.y;
		float depth = bb.max.z - bb.min.z;

		float XSteps = witdh / (CubeSteps - 1);
		float YSteps = height / (CubeSteps - 1);
		float ZSteps = depth / (CubeSteps - 1);


		for (float x = bb.min.x; x <= bb.max.x; x += XSteps)
		{
			for (float z = bb.min.z; z <= bb.max.z; z += ZSteps)
			{
				for (float y = bb.min.y; y <= bb.max.y; y += YSteps)
				{
					//Instantiate(ScenePoint, new Vector3(x, y, z), Quaternion.identity);
					transform.LookAt(new Vector3(x, y, z));

					if (CameraHandler.IsInsideBuilding(transform.position))
						yield return null;
					else
					{
					i++;
					//Instantiate(FocusPoint, transform.position, Quaternion.identity);
					yield return StartCoroutine(CameraHandler.TakeScreenshots(i));
					}
				}
			}
		}
	}

	private IEnumerator CalculateOrbitCamera(float minDistance, float maxDistance, ScreenShotMethod method)
	{
		float xDistance = (maxDistanceFocus - minDistanceFocus);

		float xIncrease = xDistance / XRadiusSteps;
		float yIncrease = YRotationAngle / YRotationSteps;
		float zIncrease = ZRotationAngle / ZRotationSteps;

		Vector3 CamPos = new Vector3(0, 0, 0);
		float tmp = yIncrease;

		

		for (float x = minDistance; x <= maxDistance; x += xIncrease)
		{
			for (float z = 0; z <= ZRotationAngle -10; z += zIncrease)
			{
				//Increase the y steps for important Views
				if (x > (maxDistance / 2) && z < ZRotationAngle / 3) yIncrease = tmp /3;
				if (x > (maxDistance * 0.75) && z < ZRotationAngle / 3)
				{
					yIncrease = tmp / 4;
				}

					for (float y = 0; y <= YRotationAngle; y += yIncrease)
					{

						CamPos.y = x * Mathf.Sin(z * Mathf.PI / 180.0f);
						CamPos.z = x * Mathf.Cos(z * Mathf.PI / 180.0f);

						CamPos.x = CamPos.z * Mathf.Sin(y * Mathf.PI / 180.0f);
						CamPos.z = CamPos.z * Mathf.Cos(y * Mathf.PI / 180.0f);

						CamPos += CalculateRandomOffset();
						transform.position = CamPos;
						//Debug.Log(i);
					yield return StartCoroutine(method());
					}
			}
		}
	}

	private Vector3 CalculateRandomOffset()
	{
		float randVal = -2;
		return new Vector3(Random.Range(-randVal, randVal), Random.Range(-randVal, randVal), Random.Range(-randVal, randVal));
	}

}
