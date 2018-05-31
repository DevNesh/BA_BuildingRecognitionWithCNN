﻿using System.Collections;
using System.IO;
using UnityEngine;

public class CameraHandler : MonoBehaviour {

	public GameObject Scene;
	public GameObject MarkedObject;
	public Material WoodenMat;
	public Material MarkedMat;
	public int AmoutScreenshot;

	private bool _isCoroutineFinished;
	private int _index;

	public string ScreenshotDir
	{
		get { return Application.streamingAssetsPath + "/ScreenShots"; }
	}


	private void Start()
	{
		_index = 0;
		_isCoroutineFinished = true;
	}

	// Update is called once per frame
	void Update ()
	{

		//if (Input.GetKeyDown("c"))
		//{
		if (_index < AmoutScreenshot && _isCoroutineFinished)
		{
			_isCoroutineFinished = false;
			transform.position = SetRandomCameraPos();
			Debug.Log("Camera Random Pos " + transform.position);
			transform.LookAt(MarkedObject.transform);
			StartCoroutine(TakeScreenshots());
		}
		//}
	}

	/// <summary>
	/// 
	/// </summary>
	/// <returns></returns>
	private Vector3 SetRandomCameraPos()
	{
		Vector3 newPosition;

		// creates a position on the positive hemisphere in terms of y
		do
		{
			newPosition = Random.insideUnitSphere * 50;
			//wird ausgeführt, bis der Ausdruck false ergibt 
			Debug.Log("inside" + IsInsideBuilding(newPosition));
		} while (newPosition.y < 3 || IsInsideBuilding(newPosition));


		return newPosition;
	}

	/// <summary>
	/// 
	/// </summary>
	public IEnumerator TakeScreenshots()
	{
		// takes a screenshot from the cameraview with the wooden material
		SetMaterialOfObject(MarkedObject, WoodenMat);
		yield return StartCoroutine(CaptureScreenshot(false));

		// takes a screenshot from the cameraview with the marked material
		SetMaterialOfObject(MarkedObject, MarkedMat);
		yield return StartCoroutine(CaptureScreenshot(true));

		_index++;
		_isCoroutineFinished = true;
	}

	/// <summary>
	/// 
	/// </summary>
	/// <param name="pos"></param>
	/// <returns></returns>
	public bool IsInsideBuilding(Vector3 pos)
	{
		foreach (Transform child in Scene.transform)
		{
			if (child.GetComponent<BoxCollider>() != null && child.GetComponent<BoxCollider>().bounds.Contains(pos))
			{
				Debug.Log("INSIDE BUILDING" + pos);
				return true;
			}

			if (child.GetComponent<SphereCollider>() != null && child.GetComponent<SphereCollider>().bounds.Contains(pos))
			{
				Debug.Log("INSIDE BUILDING" + pos);
				return true;
			}
		}
		return false;
	}

	/// <summary>
	/// 
	/// </summary>
	/// <param name="go"></param>
	/// <param name="material"></param>
	private void SetMaterialOfObject(GameObject go, Material material)
	{
		if (go.GetComponent<Renderer>() != null)
		{
			go.GetComponent<Renderer>().material = material;
			
		}
		
		foreach (Transform child in go.transform)
		{
			if (child.GetComponent<Renderer>() != null)
			{
				child.GetComponent<Renderer>().material = material;
			}
		}
	}

	/// <summary>
	/// 
	/// </summary>
	/// <param name="isMarked"></param>
	/// <returns></returns>
	IEnumerator CaptureScreenshot(bool isMarked)
	{
		// waits for the next render step, so that the material is set
		yield return new WaitForEndOfFrame();

		// setting the path
		string screenshotName = "screenshot" + _index + ".png";
		if (isMarked) screenshotName = "screenshot" + _index + "_marked" + ".png";
		string path = Path.Combine(ScreenshotDir, screenshotName);

		if (!Directory.Exists(ScreenshotDir))
		{
			Directory.CreateDirectory(ScreenshotDir);
		}

		// takes the screenshot 
		Texture2D screenImage = new Texture2D(Screen.width, Screen.height);
		
		//Get Image from screen
		screenImage.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
		screenImage.Apply();
		
		//Convert to png
		byte[] imageBytes = screenImage.EncodeToPNG();

		//Save image to file
		File.WriteAllBytes(path, imageBytes);

		Debug.Log("Screenshot was taken to: " + path);
	}



}