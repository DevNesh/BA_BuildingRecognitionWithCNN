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

	public float minDistanceFocus = 100;
	public float maxDistanceFocus = 140;

	[Header("Scene Screenshots")]
	public GameObject ScenePoint;
	public GameObject BoundingBox;

	public GameObject CamPoint;

	public float minDistanceScene = 70;
	public float maxDistanceScene = 100;

	public int CubeDevisions = 1;

	private const float ZRotationAngle = 80;
	private const float YRotationAngle = 360;

	private int i = 0;

	private void Start()
	{
		i = 3064;
	}

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
		// transform.position += Target.transform.position;
		// transform.position = new Vector3(transform.position.x, transform.position.y - Target.transform.position.y, transform.position.z);
		// transform.LookAt(Target.transform.position);

		// Look at the middle of the scene instead of the building
		Bounds bb = BoundingBox.GetComponent<BoxCollider>().bounds;
		Vector3 focusPoint = new Vector3(0, 0, 0);
		//Instantiate(FocusPoint, focusPoint, Quaternion.identity);
		transform.LookAt(focusPoint);


		if (CameraHandler.IsToCloseToViewpoint(transform.position, focusPoint) || CameraHandler.IsInsideBuilding(transform.position))
		{
			yield return null;
		}
		else
		{
			i++;
			//Instantiate(CamPoint, transform.position, Quaternion.identity);
			//Debug.Log(i);
			yield return StartCoroutine(CameraHandler.TakeScreenshots(i));
		}


	}

	private IEnumerator TakeScreenshotToAllViewPoints()
	{
		Bounds bb = BoundingBox.GetComponent<BoxCollider>().bounds;

		float witdh = bb.max.x - bb.min.x;
		float height = bb.max.y - bb.min.y;
		float depth = bb.max.z - bb.min.z;

		float XSteps = witdh / (CubeDevisions);
		float YSteps = height / (CubeDevisions);
		float ZSteps = depth / (CubeDevisions);

		Debug.Log(witdh);
		Debug.Log(height);
		Debug.Log(depth);


		for (float x = bb.min.x; x <= bb.max.x; x += XSteps)
		{
			for (float z = bb.min.z; z <= bb.max.z; z += ZSteps)
			{
				for (float y = bb.min.y; y <= bb.max.y; y += YSteps)
				{
					Vector3 focusPoint = new Vector3(x, y, z);
					//Instantiate(ScenePoint, focusPoint, Quaternion.identity);
					// transform.LookAt(focusPoint);

					if (CameraHandler.IsToCloseToViewpoint(transform.position, focusPoint)  || CameraHandler.IsInsideBuilding(transform.position) )
					{
						yield return null;
					}
					else
					{
						i++;
						Debug.Log(i);
						Instantiate(FocusPoint, transform.position, Quaternion.identity);
						yield return null; //StartCoroutine(CameraHandler.TakeScreenshots(i));
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

		float tmpY = yIncrease;
		float tmpZ = zIncrease;



		for (float x = minDistance; x <= maxDistance; x += xIncrease)
		{


			for (float z = 10; z <= ZRotationAngle -10; z += zIncrease)
			{
				//Increase the y steps for important Views
				if (x > (maxDistance / 2) && z < ZRotationAngle / 3) yIncrease = tmpY /3;
				if (x > (maxDistance * 0.75) && z < ZRotationAngle / 3)	yIncrease = tmpY / 4;

				zIncrease = (z < (ZRotationAngle / 2)) ? (tmpZ*0.75f) : tmpZ;
				Debug.Log("Ankommer: " + z);

				for (float y = 0; y <= YRotationAngle; y += yIncrease)
					{

						CamPos.y = x * Mathf.Sin(z * Mathf.PI / 180.0f);
						CamPos.z = x * Mathf.Cos(z * Mathf.PI / 180.0f);

						CamPos.x = CamPos.z * Mathf.Sin(y * Mathf.PI / 180.0f);
						CamPos.z = CamPos.z * Mathf.Cos(y * Mathf.PI / 180.0f);

						//CamPos += CalculateRandomOffset();
						transform.position = CamPos;

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
