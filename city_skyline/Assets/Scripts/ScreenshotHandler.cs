/* 
 * Copyright 2018, Danesh Wohlfart - Absolute Software GmbH, All rights reserved. 
 * Script, manages all functionality about taking the two screenshots from the scene with the camera. 
*/
using System.Collections;
using System.IO;
using UnityEngine;

public class ScreenshotHandler : MonoBehaviour {

	public GameObject Scene;			//scene with all buildings
	public GameObject MarkedObject;		//object, wihich material will be changed

	// Materials, that will be set for screenshots
	public Material WoodenMat;
	public Material MarkedMat;

	public GameObject BoundingBoxes;

	//Paths, where the screenshots will be saved 
	public string originalPath;
	public string markedPath;

	//index of the screenshot image 
	private int _index;

	/// <summary>
	/// Returns the path where the original image will be saved.
	/// </summary>	
	public string ScreenshotDir
	{
		get { return originalPath; }
	}

	/// <summary>
	/// Returns the path where the marked-object image will be saved.
	/// </summary>
	public string ScreenshotDir2
	{
		get { return markedPath; }
	}


	/// <summary>
	/// Function, calls the methods for taking both screenshots. 
	/// </summary>
	public IEnumerator TakeScreenshots(int index)
	{
		_index = index;
		// takes a screenshot from the cameraview with the wooden material
		SetMaterialOfObject(MarkedObject, WoodenMat);
		yield return StartCoroutine(CaptureScreenshot(false));

		// takes a screenshot from the cameraview with the marked material
		SetMaterialOfObject(MarkedObject, MarkedMat);
		yield return StartCoroutine(CaptureScreenshot(true));
	}

	/// <summary>
	/// Function, checks if the given point is inside an object from the scene 
	/// by checking if the point is inside the collider.
	/// </summary>
	/// <param name="pos">position that will be checked</param>
	/// <returns>True, if the given point is inside a collider of the scene. Else, false.</returns>
	public bool IsInsideBuilding(Vector3 pos)
	{
		foreach (Transform child in Scene.transform)
		{
			//check for box coliider
			if (child.GetComponent<BoxCollider>() != null && child.GetComponent<BoxCollider>().bounds.Contains(pos))
			{
				return true;
			}

			//check for sphere collider 
			if (child.GetComponent<SphereCollider>() != null && child.GetComponent<SphereCollider>().bounds.Contains(pos))
			{
				return true;
			}
		}
		return false;
	}

	/// <summary>
	/// Function, checks if the given point and the given focus point are both in one of the
	/// defined BoundingBoxes (areas) that are placed bordered to the scene.
	/// </summary>
	/// <param name="pos"></param>
	/// <returns>True, if both points are in the same defined area</returns>
	public bool IsToCloseToViewpoint(Vector3 pos, Vector3 focusPoint)
	{

		Collider col; 
		foreach (Transform child in BoundingBoxes.transform)
		{
			col = child.gameObject.GetComponent<Collider>();
			if (col.bounds.Contains(pos) && col.bounds.Contains(focusPoint))
				return true;
		}
	
		return false; 
	}

	/// <summary>
	/// Function, sets the given material on the given gameobject
	/// </summary>
	/// <param name="go">gameobject, where the material will be changed</param>
	/// <param name="material">new material, which will be set</param>
	private void SetMaterialOfObject(GameObject go, Material material)
	{
		// sets the material for gameobject
		if (go.GetComponent<Renderer>() != null)
		{
			go.GetComponent<Renderer>().material = material;
		}
		
		// sets the material for all children
		foreach (Transform child in go.transform)
		{
			if (child.GetComponent<Renderer>() != null)
			{
				child.GetComponent<Renderer>().material = material;
			}
		}
	}

	/// <summary>
	/// Function, takes a screenshot from the scene.
	/// </summary>
	/// <param name="isMarked">if true, building has marked material</param>
	/// <returns></returns>
	public IEnumerator CaptureScreenshot(bool isMarked)
	{
		// waits for the next render step, so that the material is set
		yield return new WaitForEndOfFrame();

		// setting the filename
		string screenshotName = "screenshot" + _index + ".png";

		// Create directory if not exist 
		if (!Directory.Exists(ScreenshotDir)) Directory.CreateDirectory(ScreenshotDir);
		if (!Directory.Exists(ScreenshotDir2)) Directory.CreateDirectory(ScreenshotDir2);

		string path = (!isMarked) ? Path.Combine(ScreenshotDir, screenshotName) : Path.Combine(ScreenshotDir2, screenshotName); 

		// takes the screenshot 
		Texture2D screenImage = new Texture2D(Screen.width, Screen.height);
		
		//Get Image from screen
		screenImage.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
		screenImage.Apply();
		
		//Convert to png
		byte[] imageBytes = screenImage.EncodeToPNG();

		//Save image to file
		File.WriteAllBytes(path, imageBytes);
		Destroy(screenImage);

		//Debug.Log("Screenshot was taken to: " + path);
	}
}
