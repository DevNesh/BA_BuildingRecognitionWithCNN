using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FlyHandler : MonoBehaviour {

	public GameObject Target;

	public float minDistance = 10;
	public float maxDistance = 70;

	public const float ZRotationAngle = 90;
	public const float YRotationAngle = 360;

	public float XRadiusSteps = 0;
	public float YRotationSteps = 16;
	public float ZRotationSteps = 8;

	public GameObject Cube;
	public CameraHandler CameraHandler;

	
	// Use this for initialization
	void Start () {
	}

	private void Update()
	{
		if (Input.GetKeyDown("u"))
		{
			StartCoroutine(CalculateOrbitCamera(Target.transform.position));
		}
	}

	private IEnumerator CalculateOrbitCamera(Vector3 LookAtPoint)
	{
		Debug.Log(LookAtPoint);
		float xDistance = (maxDistance - minDistance);

		float xIncrease = xDistance / XRadiusSteps;
		float yIncrease = YRotationAngle / YRotationSteps;
		float zIncrease = ZRotationAngle / ZRotationSteps;

		Vector3 CamPos = new Vector3(0, 0, 0);

		int i = 0;

		for (float x = minDistance; x <= maxDistance; x += xIncrease)
		{
			for (float z = 0; z <= ZRotationAngle -10; z += zIncrease)
			{
				for (float y = 0; y <= YRotationAngle; y += yIncrease)
				{

					CamPos.y = x * Mathf.Sin(z * Mathf.PI / 180.0f);
					CamPos.z = x * Mathf.Cos(z * Mathf.PI / 180.0f);

					CamPos.x = CamPos.z * Mathf.Sin(y * Mathf.PI / 180.0f);
					CamPos.z = CamPos.z * Mathf.Cos(y * Mathf.PI / 180.0f);

					Debug.Log("CamPos1 " + CamPos);
					CamPos = CamPos + LookAtPoint;
					Debug.Log("CamPos2 " + CamPos);

					transform.position = CamPos;
					Debug.Log("pos " + transform.position);

					transform.LookAt(LookAtPoint);

					i += 27 * 2;

					if (CameraHandler.IsInsideBuilding(transform.position))
						yield return null;
					else
					{
						Instantiate(Cube, transform.position, Quaternion.identity);
						yield return null;// StartCoroutine(CameraHandler.TakeScreenshots());
					}
				}
			}
		}
		Debug.Log(i);
	}
}
