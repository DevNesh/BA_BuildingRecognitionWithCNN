using System.Collections;
using UnityEngine;

/*
 * 
 * Copyright 2018, Danesh Wohlfart - Absolute Software GmbH, All rights reserved.
 * Script, manages all functionality about placing the camera around the scene. 
 * 
*/ 
public class CameraHandler : MonoBehaviour {

	public ScreenshotHandler ScreenshotHandler;

	[Header("Sphere Resolution Settings")]
	public float XRadiusSteps = 0;
	public float YRotationSteps = 16;
	public float ZRotationSteps = 8;

	// setting the rotation radius for the sphere algrithm
	public float minDistance = 100;
	public float maxDistance = 140;

	// setting the maximal rotations  for z and y axis
	private const float _zRotationAngle = 80;
	private const float _yRotationAngle = 360;

	[Header("Viewpoint Box")]
	public GameObject BoundingBox; 

	[Header("Points for visualisation")]
	public GameObject CamPosPoint;
	public GameObject ViewPoint;

	// resolution for the box viewpoints
	public int CubeDevisions = 1;

	[Header("Only Visulisation")]
	public bool drawPoints = false;

	// number of screenshot 
	private int _index = 0;

	// minimal height for positions of random sphere
	private const int _minHeight = 3;

	// z angle offset 
	private const int _zAngleOffset = 10;

	/// <summary>
	/// Function, will be called once when the runtime starts.
	/// </summary>
	private void Start()
	{
		_index = 0;
	}

	/// <summary>
	/// Function, will be called every frame. Starts the algorithm for screenshot taking by pressing the
	/// defined buttons.
	/// </summary>
	private void Update()
	{
		if (Input.GetKeyDown("u"))
		{
			StartCoroutine(CalculateOrbitCamera(minDistance, maxDistance, TakeScreenShotToFocusPoint));
		}

		if (Input.GetKeyDown("i"))
		{
			_index = 3064;
			StartCoroutine(CalculateOrbitCamera(minDistance, maxDistance, TakeScreenshotToAllViewPoints));
		}
	}

	/// <summary>
	/// Delegate, for method that will calculate the camera positions and take the screenshots. 
	/// </summary>
	/// <returns></returns>
	public delegate IEnumerator ScreenShotMethod();

	/// <summary>
	/// Function, sets the viewpoint of the camera to the middle on the boundig box, that is placed
	/// on the scene. Calls the method for taking the screenshots, when possible.  
	/// </summary>
	/// <returns>IEnumerator</returns>
	public IEnumerator TakeScreenShotToFocusPoint()
	{
		// Determine focuspoint 
		Vector3 focusPoint = BoundingBox.GetComponent<BoxCollider>().bounds.center; ;

		// Draw only points for visualisation 
		if (drawPoints)
		{
			if (IsPositionUsed(focusPoint)) Instantiate(ViewPoint, focusPoint, Quaternion.identity);
			Instantiate(CamPosPoint, transform.position, Quaternion.identity);
			yield return null;
		} else if (ScreenshotHandler.IsToCloseToViewpoint(transform.position, focusPoint) || ScreenshotHandler.IsInsideBuilding(transform.position))
			{
				yield return null;
			} else
				{
				_index++;
				transform.LookAt(focusPoint);
				yield return StartCoroutine(ScreenshotHandler.TakeScreenshots(_index));
			}
	}

	/// <summary>
	/// Function, calculates all the viewpoints for the camera based on the boundig box, that is placed
	/// on the scene. Calls the method for taking the screenshots, when possible.  
	/// </summary>
	/// <returns>IEnumerator</returns>
	private IEnumerator TakeScreenshotToAllViewPoints()
	{
		Bounds bb = BoundingBox.GetComponent<BoxCollider>().bounds;

		//Calculate the dimensions of the box
		float witdh = bb.max.x - bb.min.x;
		float height = bb.max.y - bb.min.y;
		float depth = bb.max.z - bb.min.z;

		//Calculate the resolution / steps for calculating the viewpoints 
		float XSteps = witdh / (CubeDevisions);
		float YSteps = height / (CubeDevisions);
		float ZSteps = depth / (CubeDevisions);

		//Calculate every viewpoint
		for (float x = bb.min.x; x <= bb.max.x; x += XSteps)
		{
			for (float z = bb.min.z; z <= bb.max.z; z += ZSteps)
			{
				for (float y = bb.min.y; y <= bb.max.y; y += YSteps)
				{
					Vector3 focusPoint = new Vector3(x, y, z);

					// Draw only points for visualisation
					if (drawPoints)
					{
						if (IsPositionUsed(focusPoint)) Instantiate(ViewPoint, focusPoint, Quaternion.identity);
						Instantiate(CamPosPoint, transform.position, Quaternion.identity);
						yield return null; 
					} else if (ScreenshotHandler.IsToCloseToViewpoint(transform.position, focusPoint) || ScreenshotHandler.IsInsideBuilding(transform.position))
					{
						yield return null;
					}
					else
					{
						_index++;
						transform.LookAt(focusPoint);
						yield return StartCoroutine(ScreenshotHandler.TakeScreenshots(_index));
					}
				}
			}
		}
	}

	/// <summary>
	/// Function, calculates all the camera positions. Places the camera around the scene.
	/// Positions are calculated around the scene like a voluminous sphere. At every position a 
	/// defined method is called. 
	/// </summary>
	/// <param name="minDistance">Radius, where the first camera positions will be set</param>
	/// <param name="maxDistance">Radius, where the last camera positions will be set</param>
	/// <param name="method">Method that is called at every single camera position</param>
	/// <returns>IEnumerator</returns>
	private IEnumerator CalculateOrbitCamera(float minDistance, float maxDistance, ScreenShotMethod method)
	{
		// Calculate the increasement for every dimension per loop pass
		float xDistance = (maxDistance - minDistance);
		float xIncrease = xDistance / XRadiusSteps;
		float yIncrease = _yRotationAngle / YRotationSteps;
		float zIncrease = _zRotationAngle / ZRotationSteps;

		float initialYIncrease = yIncrease;
		float initialZIncrease = zIncrease;

		// temporary variable for the position of the camera 
		Vector3 CamPos = new Vector3(0, 0, 0);

		for (float x = minDistance; x <= maxDistance; x += xIncrease)
		{
			for (float z = _zAngleOffset; z <= _zRotationAngle - _zAngleOffset; z += zIncrease)
			{
				// Optimization: Increase the y steps for a balanced set of positions
				if (x > (maxDistance / 2) && z < _zRotationAngle / 3) yIncrease = initialYIncrease / 3;
				if (x > (maxDistance * 0.75) && z < _zRotationAngle / 3) yIncrease = initialYIncrease / 4;

				// Optimization: Increase the z steps for a balanced set of positions
				zIncrease = (z < (_zRotationAngle / 2)) ? (initialZIncrease * 0.75f) : initialZIncrease;

				for (float y = 0; y <= _yRotationAngle; y += yIncrease)
				{
					CamPos.y = x * Mathf.Sin(z * Mathf.PI / 180.0f);
					CamPos.z = x * Mathf.Cos(z * Mathf.PI / 180.0f);

					CamPos.x = CamPos.z * Mathf.Sin(y * Mathf.PI / 180.0f);
					CamPos.z = CamPos.z * Mathf.Cos(y * Mathf.PI / 180.0f);

					// CamPos += CalculateRandomOffset(); (Old implementation, where an offset will be added to the positions)
					transform.position = CamPos;
					yield return StartCoroutine(method());
				}
			}
		}
	}

	/// <summary>
	/// Function, (old, is not used anymore),
	/// sets a random camera position inside a defined sphere. The placement of the sphere is centered.
	/// Restrictions where made, that the position will be at the upper half of the sphere. 
	/// </summary>
	/// <param name="sphereRadius">Defines the radius of the sphere</param>
	/// <returns>New random position</returns>
	private Vector3 SetRandomCameraPos(int sphereRadius)
	{
		Vector3 newPosition;

		// creates a position on the positive hemisphere in terms of y
		do
		{
			newPosition = Random.insideUnitSphere * sphereRadius;
		} while (newPosition.y < _minHeight || ScreenshotHandler.IsInsideBuilding(newPosition));

		return newPosition;
	}

	/// <summary>
	/// Function (old, is not used anymore),
	/// calculates a vector, where all components from the vector are random values based on the input.
	/// The random values will be in a range from -input to +input.
	/// </summary>
	/// <returns></returns>
	private Vector3 CalculateRandomOffset(int value)
	{
		return new Vector3(Random.Range(-value, value), Random.Range(-value, value), Random.Range(-value, value));
	}

	/// <summary>
	/// Function, checks if there is already a sphere spawned at the given position.
	/// </summary>
	/// <param name="targetPos">Position that will be checked</param>
	/// <returns>True if there is a sphere already spawned, false if not</returns>
	public bool IsPositionUsed(Vector3 targetPos)
	{
		GameObject[] viewpoints = GameObject.FindGameObjectsWithTag("viewpoint");
		foreach (GameObject current in viewpoints)
		{
			if (current.transform.position == targetPos)
				return false;
		}
		return true;
	}
}
